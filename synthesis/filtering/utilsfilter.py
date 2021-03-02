#import ffmpeg
from pydub import AudioSegment
from scipy.io import wavfile
#from plotly.offline import init_notebook_mode
#import plotly.graph_objs as go
#import plotly
import numpy as np
import matplotlib.pyplot as plt
import IPython
import parselmouth
from parselmouth.praat import call

# Code inspired from 
# https://hackernoon.com/audio-handling-basics-how-to-process-audio-files-using-python-cli-jo283u3y

# retuns sample rate and wav data
def get_wav(path):
    return wavfile.read(path)

# start and end in seconds
# returns new data and new time length
def trim(wavdata, start, end, fs_wav):
    return wavdata[int(start * fs_wav): int(end * fs_wav)], \
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

