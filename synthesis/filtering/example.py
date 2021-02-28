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
    testpath = './testdata/smaller7tmono.wav'
    fs_wav, data_wav = get_wav(testpath)
    seg = Segment(testpath, 1, 3)
    print("Amplitude")
    seg.draw_data()
    seg.write("test.wav")
    plt.show()
main()

