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
from parselmouth.praat import call

class Segment:
    # todo extract parts
    def __init__(self, path, start_time, end_time):
        self.path = path
        self.snd = parselmouth.Sound(path)
        self.data = self.snd.values.T # amplitudes
        self.start_time = start_time
        self.end_time = end_time
        self.spectrogram = self.snd.to_spectrogram()
        self.intensity = self.snd.to_intensity()
        self.pitch_obj = self.snd.to_pitch()
        self.pitch = self.pitch_obj.selected_array['frequency']
        # pre-emphasize
        self.snd_emp = self.snd.copy().pre_emphasize()

    #def write(self,path):
    #   wavfile.write(path, self.snd.sampling_frequency,self.snd.values) 

    def pitch_avg(self):
        return np.average(self.pitch)

    def intensity_avg(self):
        return np.average(self.intensity)
    
    def get_speech_rate(self):
        return 1

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

