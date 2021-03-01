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
from parselmouth.praat import call
from utilsfilter import *
from segment import Segment

def main():
    #testpath = './testdata/smaller7tmono.wav'
    testpath = './testdata/7quCH1LZWMKX9xg2tJBMsP.wav'
    fs_wav, data_wav = get_wav(testpath)
    print("fs wav: ", fs_wav)
    #samp_freq = 
    fs = 44100.0
    seg = Segment(testpath, 5, 19, fs)
    #print("Amplitude")
    #seg.draw_data()
    #seg.write("test.wav")
    #plt.show()
    #sr = seg.get_speech_rate()
    #print("SPEECH RATE:" , sr)
main()

