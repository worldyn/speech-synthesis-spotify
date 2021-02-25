import ffmpeg
from pydub import AudioSegment
from scipy.io import wavfile
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
import plotly
import numpy as np
import matplotlib.pyplot as plt
import IPython


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

def main():
    path = './testdata/smaller7tmono.wav'
    fs_wav, data_wav = get_wav(path) # sampling rate and audio data

    # normalize, assumes 16 bits per sample
    data_wav_norm = data_wav / (2**15)

    segments = segment_interval(data_wav_norm, fs_wav, 1)
    data_no_silence = remove_silent_segments(segments)

    write_wav("./testdata/nosilence.wav",data_no_silence,fs_wav)

    plt.plot(data_wav_norm)
    plt.show()

main()

