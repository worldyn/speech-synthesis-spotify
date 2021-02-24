import os
from pathlib import Path
from functools import partial

import numpy as np
from multiprocessing import Pool

from scipy import signal
from scipy import io
from scipy.io import wavfile

import soundfile

from PIL import Image

import keras

from .helpers import (
    load_wav,
    create_melspec,
    normalise,
    zcr_rate,
    list_filenames,
    colorvec,
    colorvec2,
    textgrid2annot,
    annot2textgrid,
)


input_path = Path("./audio/show_60aEckwTYs8xCEpsAasV0o/3NHTGeZoLLIfoHnlwtOu6w.wav")
output_root = Path("./output")

output_path = output_root / input_path.stem
output_path.mkdir(parents=True)

sample_rate = 44100


# load input wav and split into two second samples
seconds_per_split = 2
read_filename, wav_out, num_samples, sample_freq = load_wav(
    input_path.as_posix(), sr=sample_rate
)
num_splits = num_samples // (seconds_per_split * sample_rate)
one_channel_out = wav_out[:, 0]  # only use left channel
wav_in = np.reshape(
    one_channel_out[: seconds_per_split * sample_rate * num_splits],
    (num_splits, seconds_per_split * sample_rate),
)

# create mel-spectrogram
pool = Pool()
ins = [wav_in[r, :] for r in range(num_splits)]

melspecs = pool.map(create_melspec, ins)

# use zero crossing rate to create zcr-colored melspectrograms
zrates = pool.map(zcr_rate, ins)
func = partial(colorvec, melspecs, zrates)
col_in = [(melspecs[r], zrates[r]) for r in range(num_splits)]
colspecs = pool.map(colorvec2, col_in)
x_complete = np.asarray(colspecs).astype(np.float32)
print(np.shape(x_complete))

# save the zcr-coloured melspectrograms
zcr_path = output_root / "zcrgrams" / input_path.stem
zcr_path.mkdir(parents=True)

for n in range(0, np.shape(x_complete)[0]):
    imout = np.floor(255 * x_complete[n, ::-1, :, :])
    imout = imout.astype(np.uint8)
    img = Image.fromarray(imout, "RGB")
    img.save(
        zcr_path / ("zcr" + f"{n:04d}" + ".png"),
        "PNG",
    )

soundfile.write(input_path.stem + ".wav", wav_out, sample_freq, subtype="PCM_16")
