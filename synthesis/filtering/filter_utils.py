import ffmpeg
from pydub import AudioSegment
from scipy.io import wavfile
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
import plotly
import numpy as np
import matplotlib.pyplot as plt
import IPython
import parselmouth


# Great help from: https://hackernoon.com/audio-handling-basics-how-to-process-audio-files-using-python-cli-jo283u3y

# retuns sample rate and wav data
def get_wav(path):
    return wavfile.read(path)

# start and end in seconds
def trim(wavdata, start, end, sampling_freq):
    return wavdata[start * fs_wav: end * fs_wav], \
            np.arange(0, len(wavdata)) / fs_wav 

# segment into equal sized segments
# assumes wav data is normalized
# segment_size_t in s
def segment_interval(signal, fs, segment_size_t):
    signal_len = len(signal)
    segment_size = segment_size_t * fs
    segments = np.array([signal[x:x + segment_size] for x in
                         np.arange(0, signal_len, segment_size)])
    return segments

# assumes normalized audio wav data segments
def remove_silent_segments(segments, energy_thres=0.5):
    energies = [(s**2).sum() / len(s) for s in segments]
    # integer overflow would occure without normalization here!
    thres = energy_thres * np.median(energies)
    index_of_segments_to_keep = (np.where(energies > thres)[0])
    # get segments that have energies higher than a the threshold:
    segments2 = segments[index_of_segments_to_keep]
    # concatenate segments to signal:
    return np.concatenate(segments2)

def write_wav(path, signal, fs):
    wavfile.write(path, fs, signal)

def plot_sound(path):
    snd = parselmouth.Sound("./testdata/smaller7tmono.wav")
    plt.figure()
    plt.plot(snd.xs(), snd.values.T)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
    plt.show()

class Sound:
    # todo extract parts
    def __init__(self, path):
        self.data = parselmouth.Sound(path)
        self.spectrogram = self.data.to_spectrogram()
        self.intensity = self.data.to_intensity()
        self.pitch_obj = self.data.to_pitch()
        self.pitch = self.pitch_obj.selected_array['frequency']
        # pre-emphasize
        self.data_emp = self.data.copy().pre_emphasize()

    def pitch_avg(self):
        return np.average(self.pitch)

    def intensity_avg(self):
        return np.average(self.intensity)

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

def main():
    # TODO: 
    # silence removal (done)
    # trim (done)
    # speech rate (spotify paper)
    # music?
    path = './testdata/smaller7tmono.wav'
    fs_wav, data_wav = get_wav(path) # sampling rate and audio data

    # normalize, assumes 16 bits per sample
    #data_wav_norm = data_wav / (2**15)

    #segments = segment_interval(data_wav_norm, fs_wav, 1)
    #data_no_silence = remove_silent_segments(segments)

    #write_wav("./testdata/nosilence.wav",data_no_silence,fs_wav)

    #plt.plot(data_wav_norm)
    snd = Sound("./testdata/smaller7tmono.wav")
    #snd.draw_intensity()
    #snd.draw_spectrogram()
    snd.draw_pitch()

    plt.show()

main()

