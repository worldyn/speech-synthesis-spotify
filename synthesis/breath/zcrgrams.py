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

from tqdm.auto import tqdm

from .helpers import (
    load_wav,
    create_melspec,
    zcr_rate,
    colorvec,
    colorvec2,
)


show_id = "0L0j6X6cf3DO1Bs0D0K4Ch"


def process_file(path: Path):
    sample_rate = 44100

    # load input wav and split into two second samples
    seconds_per_split = 2
    read_filename, wav_out, num_samples, sample_freq = load_wav(
        path.as_posix(), sr=sample_rate
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
    zcr_path = Path(path.stem)
    zcr_path.mkdir(parents=True)

    for n in range(0, np.shape(x_complete)[0]):
        imout = np.floor(255 * x_complete[n, ::-1, :, :])
        imout = imout.astype(np.uint8)
        img = Image.fromarray(imout, "RGB")
        img.save(
            zcr_path / ("zcr" + f"{n:04d}" + ".png"),
            "PNG",
        )


if __name__ == "__main__":
    show_path = Path(f"./audio/show_{show_id}")
    for file_path in tqdm(show_path.iterdir()):
        process_file(show_path)
