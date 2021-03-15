from pathlib import Path
import json
import numpy as np
import soundfile
from tqdm.auto import tqdm

train_filename = "ljs_audio_text_train_filelist.txt"
val_filename = "ljs_audio_text_val_filelist.txt"
test_filename = "ljs_audio_text_test_filelist.txt"

target_sample_rate = 22050
audio_dir = Path("ljs_dataset_folder/wavs")

train_fraction = 0.95
val_fraction = 0.04
test_fraction = 0.01


def prepare_annotations():
    assert train_fraction + val_fraction + test_fraction <= 1.0
    print("=> Loading annotations...")
    with open("filtered/filtered.json") as file:
        segments = json.load(file)

    audio_paths = segments["paths"]
    transcripts = segments["transcripts"]

    assert len(audio_paths) == len(transcripts)
    print("=> Data Loaded...")

    n_data = len(audio_paths)
    n_train = int(train_fraction * n_data)
    n_val = int(val_fraction * n_data)
    n_test = int(test_fraction * n_data)
    print(f"=> Number of data points in total: {n_data}")
    print(f"=> n_train {n_train}, n_val {n_val}, n_test {n_test}")

    assert n_train + n_val + n_test <= n_data

    def write_file(path, start_index, end_index):
        with open(path, "w") as file:
            for i in range(start_index, end_index):
                audio_path = (Path("filelists") / audio_dir / audio_paths[i]).as_posix()
                text = transcripts[i]
                file.write(audio_path + "|" + text + "\n")

    train_idx = n_train
    val_idx = train_idx + n_val
    test_idx = val_idx + n_test

    write_file(train_filename, 0, train_idx)
    write_file(val_filename, train_idx, val_idx)
    write_file(test_filename, val_idx, test_idx)


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
