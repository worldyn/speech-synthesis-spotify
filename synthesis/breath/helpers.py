#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 21:50:09 2018
helper functions for stp_episode 
@author: szekely
interpreter: std spyder
"""

#
import os
import numpy as np
from skimage.measure import block_reduce
from scipy import signal
from scipy import io
from scipy.io import wavfile

import librosa
import librosa.display


def load_wav(fn, sr=None, normalize=True):
    if fn == "":  # ignore empty filenames
        print("filename missing")
        return None
    fs, audio = wavfile.read(fn)
    audio = audio.astype(np.float32)
    duration = np.shape(audio)[0]
    if duration == 0:  # ignore zero-length samples
        print("sample has no length")
        return None
    if sr != fs and sr != None:
        audio = librosa.resample(audio, fs, sr)
        fs = sr
    max_val = np.abs(audio).max()
    if max_val == 0:  # ignore completely silent sounds
        print("silent sample")
        return None
    if normalize:
        audio = audio / max_val
    # audio = audio.astype(np.int16)
    return (fn, audio, duration, fs)


def create_melspec(wav_in, sr=None, n_fft=960, hop_length=120, n_mels=128):
    if sr == None:
        sr = min(48000, len(wav_in) // 2)
        n_fft = sr // 50
        hop_length = sr // 400
    S = librosa.feature.melspectrogram(
        wav_in, power=1, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels
    )
    # log_S = librosa.amplitude_to_db(S, ref=np.max)
    log_S = librosa.amplitude_to_db(S, ref=np.max)
    melspecs = np.asarray(log_S).astype(np.float32)
    return melspecs


def normalise(y):
    if np.amax(y) == np.amin(y):
        print("ERROR: max and min values are equal")
        return None
    y = (y - np.amin(y)) / (np.amax(y) - np.amin(y))
    return y


def zcr_rate(wav_in, step=240, sz=960):
    # if len(wav_in) < 2*48000:
    #    sz = len(wav_in) // (2*50)
    #    step = len(wav_in) // (2*200)
    cross = np.abs(np.diff(np.sign(wav_in + 1e-8)))
    cross[cross > 1] = 1
    steps = int((np.shape(cross)[0] - sz) / step)
    zrate = np.zeros((steps,))
    for i in range(steps):
        zrate[i] = np.mean(cross[i * step : i * step + sz])
    return zrate


def colorvec(
    spec,
    zcrate,
    maxzcr=0.4,
    low_slow=np.array([0.0, 255.0, 255.0]),
    low_fast=np.array([255.0, 255.0, 255.0]),
    high_slow=np.array([0.0, 0.0, 0.0]),
    high_fast=np.array([255.0, 0.0, 0.0]),
):
    zcr2 = np.interp(
        range(np.shape(spec)[1]),
        np.linspace(0, np.shape(spec)[1], np.shape(zcrate)[0]),
        zcrate,
    )
    spec2 = np.abs(spec) / 80
    outp = np.zeros((np.shape(spec2)[0], np.shape(spec2)[1], 3))
    z = zcr2 / maxzcr
    z[z > 1] = 1
    low = np.outer(low_slow, np.ones_like(z)) + np.outer(low_fast - low_slow, z)
    high = np.outer(high_slow, np.ones_like(z)) + np.outer(high_fast - high_slow, z)
    for k in range(3):
        outp[:, :, k] = np.tile(low[k, :], (np.shape(spec2)[0], 1)) + spec2 * np.tile(
            high[k, :] - low[k, :], (np.shape(spec2)[0], 1)
        )
    outp = outp / 255
    return outp


def colorvec2(
    inp,
    maxzcr=0.4,
    low_slow=np.array([0.0, 255.0, 255.0]),
    low_fast=np.array([255.0, 255.0, 255.0]),
    high_slow=np.array([0.0, 0.0, 0.0]),
    high_fast=np.array([255.0, 0.0, 0.0]),
):
    zcr2 = np.interp(
        range(np.shape(inp[0])[1]),
        np.linspace(0, np.shape(inp[0])[1], np.shape(inp[1])[0]),
        inp[1],
    )
    spec2 = np.abs(inp[0]) / 80
    outp = np.zeros((np.shape(spec2)[0], np.shape(spec2)[1], 3))
    z = zcr2 / maxzcr
    z[z > 1] = 1
    low = np.outer(low_slow, np.ones_like(z)) + np.outer(low_fast - low_slow, z)
    high = np.outer(high_slow, np.ones_like(z)) + np.outer(high_fast - high_slow, z)
    for k in range(3):
        outp[:, :, k] = np.tile(low[k, :], (np.shape(spec2)[0], 1)) + spec2 * np.tile(
            high[k, :] - low[k, :], (np.shape(spec2)[0], 1)
        )
    outp = outp / 255
    return outp
