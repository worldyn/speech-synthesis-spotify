import os
import time
import logging
import threading
import time
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile


LOCAL_DATA_ROOT = './data/spotify-podcasts-2020/podcasts-transcripts/6/0'

REMOTE_AUDIO_ROOT = './Spotify-Podcasts-2020/podcasts-audio-only-2TB/podcasts-audio/6/0'

REMOTE_TRANSCRIPT_ROOT = './Spotify-Podcasts-2020/podcasts-no-audio-13GB/6/0'


def collect_files():

    podcasts_ids = []

    for subdir, dirs, files in os.walk(LOCAL_DATA_ROOT):
        for filename in files:

            podcast_id = filename.split('.')[0]

            file = subdir.replace('\\','/') + '/' + podcast_id + '.wav'

            print(file)

            exit()

            podcasts_ids.append((subdir, podcast_id))


def make_spectrogram(batch):
    sample_rate, samples = wavfile.read('path-to-mono-audio-file.wav')
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()


collect_files()