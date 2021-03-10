from pathlib import Path
import json
import numpy as np
import soundfile
from tqdm.auto import tqdm

# Constants
input_filename = "filtered_show.json"
train_filename = "ljs_audio_text_train_filelist.txt"
val_filename = "ljs_audio_text_val_filelist.txt"
test_filename = "ljs_audio_text_test_filelist.txt"

target_sample_rate = 22050
audio_dir = Path("ljs_dataset_folder/wavs")

train_fraction = 0.95
val_fraction = 0.04
test_fraction = 0.01


def prepare_annotations():
    # Loading the intervals from INTERVAL_FILE
    assert train_fraction + val_fraction + test_fraction == 1.0
    print("=> Loading annotations...")
    with open(Path("filtered") / input_filename) as file:
        segments = json.load(file)

    # Loading the data
    paths = segments["paths"]
    # timestamps = segments["timestamps"]
    transcripts = segments["transcripts"]

    assert len(paths) == len(transcripts)
    print("=> Data Loaded...")

    n_data = len(paths)
    n_train = int(train_fraction * n_data)
    n_val = int(val_fraction * n_data)
    n_test = int(test_fraction * n_data)
    print(f"=> Number of data points in total: {n_data}")
    print(f"=> n_train {n_train}, n_val {n_val}, n_test {n_test}")

    # remove from test if too big
    if n_train + n_val + n_test > n_data:
        n_test -= n_train + n_val + n_test - n_data

    assert n_train + n_val + n_test <= n_data

    train_idx = n_train
    val_idx = train_idx + n_val
    test_idx = val_idx + n_test

    print("=> Writing Tacotron Train data file...")
    with open(train_filename, "w") as f:
        for i in range(0, train_idx):
            path = paths[i]
            text = transcripts[i]
            f.write(path + "|" + text + "\n")

    print("=> Writing Tacotron Validation data file...")
    with open(val_filename, "w") as f:
        for i in range(train_idx, val_idx):
            path = paths[i]
            text = transcripts[i]
            f.write(path + "|" + text + "\n")

    print("=> Writing the rest to Tacotron test data file...")
    with open(test_filename, "w") as f:
        for i in range(val_idx, test_idx):
            path = paths[i]
            text = transcripts[i]
            f.write(path + "|" + text + "\n")

    print("=> Write complete...")


def prepare_audio():
    print("Preparing audio...")
    audio_dir.mkdir(parents=True)
    input_paths = list(Path("filtered").glob("*.wav"))
    for input_path in tqdm(input_paths):
        audio_clip, original_sample_rate = soundfile.read(input_path.as_posix())
        assert original_sample_rate % target_sample_rate == 0
        soundfile.write(
            file=audio_dir / input_path.name,
            data=audio_clip[:: original_sample_rate // target_sample_rate, 0],
            samplerate=target_sample_rate,
        )


if __name__ == "__main__":
    prepare_annotations()
    prepare_audio()
