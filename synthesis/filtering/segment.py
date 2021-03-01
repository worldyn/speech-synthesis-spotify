# import ffmpeg
from pydub import AudioSegment
from scipy.io import wavfile
#from plotly.offline import init_notebook_mode
#import plotly.graph_objs as go
#import plotly
import numpy as np
import matplotlib.pyplot as plt
import IPython
from IPython.display import Audio
import parselmouth
from parselmouth.praat import call, run_file
import pickle
import myprosody as mysp
import os
from os.path import join
import pyacoustics
from pyacoustics.signals import audio_scripts
from pyacoustics.speech_rate import uwe_sr
from pyacoustics.utilities import utils
from pyacoustics.utilities import my_math

class Segment:
    # todo extract parts
    def __init__(self, path, start_time, end_time):
        self.path = path
        self.snd = parselmouth.Sound(path)
        self.data = self.snd.values.T # amplitudes
        self.start_time = start_time
        self.end_time = end_time
        #self.spectrogram = self.snd.to_spectrogram()
        self.intensity = self.snd.to_intensity()
        self.pitch_obj = self.snd.to_pitch()
        self.pitch = self.pitch_obj.selected_array['frequency']
        self.energy = self.snd.get_energy()
        # pre-emphasize
        #self.snd_emp = self.snd.copy().pre_emphasize()

    #def write(self,path):
    #   wavfile.write(path, self.snd.sampling_frequency,self.snd.values) 

    def pitch_avg(self):
        return np.average(self.pitch)

    def get_energy(self):
        return self.energy

    def intensity_avg(self):
        return np.average(self.intensity)
    
    def get_speech_rate(self):
        #_rootDir = "/Users/tmahrt/Dropbox/workspace/pyAcoustics/examples/files"
        _rootDir = "./"
        _wavPath = _rootDir
        _syllableNucleiPath = join(_rootDir, "syllableNuclei_portions")
        _matlabEXE = "/Applications/MATLAB_R2014a.app/bin/matlab"
        _matlabScriptsPath = ("pyAcoustics/"
                              "matlabScripts")

        getSpeechRateForIntervals(
            _wavPath, _syllableNucleiPath, 
            _matlabEXE, _matlabScriptsPath
        )

    def draw_data(self):
        plt.plot(self.data)

    def draw_spectrogram(self, dynamic_range=70):
        X, Y = self.spectrogram.x_grid(), self.spectrogram.y_grid()
        sg_db = 10 * np.log10(self.spectrogram.values)
        plt.pcolormesh(
            X,Y,sg_db,vmin=sg_db.max() - dynamic_range,cmap='afmhot'
        )
        plt.ylim([self.spectrogram.ymin, self.spectrogram.ymax])
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")

    def draw_intensity(self):
        plt.plot(
            self.intensity.xs(), self.intensity.values.T, 
            linewidth=3, color='g'
        )
        plt.plot(self.intensity.xs(), self.intensity.values.T, linewidth=1)
        plt.grid(False)
        plt.ylim(0)
        plt.ylabel("intensity [dB]")

    def draw_pitch(self):
        pitch_values = self.pitch
        pitch_values[pitch_values == 0] = np.nan
        plt.plot(
            self.pitch_obj.xs(), pitch_values, 'o',
            markersize=5, color='w'
        )
        plt.plot(self.pitch_obj.xs(), pitch_values, 'o', markersize=2)
        plt.grid(False)
        plt.ylim(0, self.pitch_obj.ceiling)
        plt.ylabel("fundamental frequency [Hz]")


def praat_speech_rate(wavpath):
    """
    Measure the rate of speech (speed)
    """
    z2 = run_praat_file(wavpath)
    z3=int(z2[2]) # will be the integer number 10
    #z4=float(z2[3]) # will be the floating point number 8.3
    print ("rate_of_speech=",z3,"# syllables/sec original duration")
    return z3

def run_praat_file(wavpath):
    """
    p : path to dataset folder
    m : path to file
    returns : objects outputed by the praat script
    """
    sound = wavpath
    praatscript = "speechrate.praat"
    path="."

    assert os.path.isfile(sound), "Wrong path to audio file"
    assert os.path.isfile(praatscript), "Wrong path to praat script"
    #assert os.path.isdir(path), "Wrong path to audio files"
    print("calculating speech rate...")

    try:
        objects = run_file(
            praatscript, -20, 2, 0.3,
            "yes",sound,path, 80, 400,
            0.01, capture_output=True
        )

        print("Sound obj: ",objects[0]) # parselmouth sound object 
        z1=str( objects[1]) #  parselmouth.Data object
        z2=z1.strip().split()
        return z2
    except:
        z3 = 0
        print ("Try again the sound of the audio was not clear")

def _runSpeechRateEstimate(wavPath, syllableNucleiPath, matlabEXE,
                           matlabScriptsPath, printCmd=True):
    uwe_sr.findSyllableNuclei(wavPath, syllableNucleiPath, matlabEXE,
                              matlabScriptsPath, printCmd)


def _runSpeechRateEstimateOnIntervals(wavPath, tgPath, tierName, wavTmpPath,
                                      syllableNucleiPath, matlabEXE,
                                      matlabScriptsPath, printCmd=True,
                                      outputTGFlag=False):

    utils.makeDir(wavTmpPath)
    # Split audio files into subsections based on textgrid intervals
    for name in utils.findFiles(wavPath, filterExt=".wav", stripExt=True):
        praatio_scripts.splitAudioOnTier(join(wavPath, name + ".wav"),
                                         join(tgPath, name + ".TextGrid"),
                                         tierName, wavTmpPath, outputTGFlag)

    uwe_sr.findSyllableNuclei(wavTmpPath, syllableNucleiPath, matlabEXE,
                              matlabScriptsPath, printCmd)



def _addSyllableNucleiToTextgrids(wavPath, tgPath, tierName,
                                 syllableNucleiPath, outputPath):
    # Add syllable nuclei to textgrids
    for name in utils.findFiles(wavPath, filterExt=".wav", stripExt=True):

        tg = tgio.openTextgrid(join(tgPath, name + ".TextGrid"))
        entryList = tg.tierDict[tierName].entryList
        startTimeList = [entry[0] for entry in entryList]
        nucleusSyllableList = uwe_sr.toAbsoluteTime(name, syllableNucleiPath,
                                                    startTimeList)
        flattenedSyllableList = [nuclei for sublist in nucleusSyllableList
                                 for nuclei in sublist]
        wavFN = join(wavPath, name + ".wav")
        duration = audio_scripts.getSoundFileDuration(wavFN)

        oom = my_math.orderOfMagnitude(len(flattenedSyllableList))
        labelTemplate = "%%0%dd" % (oom + 1)

        entryList = [(timestamp, labelTemplate % i)
                     for i, timestamp in enumerate(flattenedSyllableList)]
        print(flattenedSyllableList)
        tier = tgio.PointTier("Syllable Nuclei", entryList, 0, duration)

        tgFN = join(tgPath, name + ".TextGrid")
        tg = tgio.openTextgrid(tgFN)
        tg.addTier(tier)
        tg.save(join(outputPath, name + ".TextGrid"))


def _calculateSyllablesPerSecond(wavPath, syllableNucleiPath):

    for name in utils.findFiles(wavPath, filterExt=".wav", stripExt=True):
        nucleusSyllableList = uwe_sr.toAbsoluteTime(name, syllableNucleiPath,
                                                    [0, ])
        nucleusSyllableList = [nucleus for subList in nucleusSyllableList
                               for nucleus in subList]
        numSyllables = len(nucleusSyllableList)
        wavFN = join(wavPath, name + ".wav")
        duration = audio_scripts.getSoundFileDuration(wavFN)

        print("%s - %.02f syllables/second" %
              (name, numSyllables / float(duration)))


def _calculateSyllablesPerSecondForIntervals(wavPath, tgPath, tierName,
                                             syllableNucleiPath):
    # Add syllable nuclei to textgrids
    for name in utils.findFiles(wavPath, filterExt=".wav", stripExt=True):

        tg = tgio.openTextgrid(join(tgPath, name + ".TextGrid"))
        entryList = tg.tierDict[tierName].entryList
        startTimeList = [entry[0] for entry in entryList]
        nucleusSyllableList = uwe_sr.toAbsoluteTime(name, syllableNucleiPath,
                                                    startTimeList)

        durationList = []
        for intervalList, entry in utils.safeZip([nucleusSyllableList,
                                                  entryList],
                                                 enforceLength=True):
            start, stop = entry[0], entry[1]
            duration = len(intervalList) / (stop - start)
            durationList.append(str(duration))

        print("%s - %s (syllables/second for each interval)" %
              (name, ",".join(durationList)))


def markupTextgridWithSyllableNuclei(wavPath, tgPath, tierName, wavTmpPath,
                                     syllableNucleiPath, matlabEXE,
                                     matlabScriptsPath, outputPath,
                                     printCmd=True, outputTGFlag=False):

    utils.makeDir(outputPath)

    # This can be commented out and instead, you can run the code directly
    # from matlab, then you can start directly from the next line
    _runSpeechRateEstimateOnIntervals(wavPath, tgPath, tierName, wavTmpPath,
                                      syllableNucleiPath, matlabEXE,
                                      matlabScriptsPath, printCmd,
                                      outputTGFlag)

    _addSyllableNucleiToTextgrids(wavPath, tgPath, tierName,
                                  syllableNucleiPath, outputPath)

    _calculateSyllablesPerSecondForIntervals(wavPath, tgPath, tierName,
                                             syllableNucleiPath)


def getSpeechRateForIntervals(wavPath, syllableNucleiPath, matlabEXE,
                              matlabScriptsPath, printCmd=True):

    # This can be commented out and instead, you can run the code directly
    # from matlab, then you can start directly from the next line
    _runSpeechRateEstimate(wavPath, syllableNucleiPath, matlabEXE,
                           matlabScriptsPath, printCmd)

    _calculateSyllablesPerSecond(wavPath, syllableNucleiPath)


