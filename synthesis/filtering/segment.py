from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import parselmouth
from utilsfilter import *
from g2p_en import G2p

# Uses the parselmouth library for audio data usage
# https://parselmouth.readthedocs.io

class Segment:
    # todo extract parts
    def __init__(self, path, start_time, end_time, samp_freq = 44100, text=''):
        self.path = path
        self.start_time = start_time
        self.end_time = end_time
        self.time = end_time - start_time
        self.snd = parselmouth.Sound(path)
        self.data = self.snd.values.T # amplitudes
        self.samp_freq = samp_freq
        #self.spectrogram = self.snd.to_spectrogram()
        self.snd = parselmouth.Sound(path)
        self.intensity = self.snd.to_intensity()
        self.pitch_obj = self.snd.to_pitch()
        self.pitch = self.pitch_obj.selected_array['frequency']
        self.energy = self.snd.get_energy()
        self.text = text
        # pre-emphasize
        #self.snd_emp = self.snd.copy().pre_emphasize()

    def write(self,path):
       wavfile.write(path, self.samp_freq, self.data) 

    def pitch_avg(self):
        return np.average(self.pitch)

    def get_energy(self):
        return self.energy

    def intensity_avg(self):
        return np.average(self.intensity)
    
    def get_speech_rate(self):
        # Uses g2pE for phoneme conversion
        # https://github.com/Kyubyong/g2p
        g2p = G2p()
        phonemes = g2p(self.text)
        phonemes = [s for s in phonemes if s.strip()]
        return len(phonemes) / self.time

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
