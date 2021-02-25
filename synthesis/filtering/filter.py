import ffmpeg
from pydub import AudioSegment
from scipy.io import wavfile
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
import plotly
import numpy as np
import matplotlib.pyplot as plt

path = './testdata/smaller7tmono.wav'

fs_wav, data_wav = wavfile.read(path) # sampling rate and audio data

# normalize, assumes 16 bits per sample
data_wav_norm = data_wav / (2**15)

time_wav = np.arange(0, len(data_wav)) / fs_wav
plt.plot(data_wav)
plt.show()



