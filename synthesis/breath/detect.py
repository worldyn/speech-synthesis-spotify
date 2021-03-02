from pathlib import Path
import numpy as np
import cv2
import keras
from tqdm.auto import tqdm


nr_speakers = 1  # pretrained model is single speaker

# output settings
n_mels = 128
num_slices = 40  # num_slices in keras model, standard 2 seconds with 20 steps each
slicepersec = 400

# corpus creation settings
max_utt = 12  # maximum utterance length (seconds)
min_utt = 1.0  # minimum utterance length (seconds)
trail = 0.02  # silence before and after utterance (seconds)
trailfr = 0  # additional frame(s) included for smoother end of utterance (1 for TCC / 0 for Obama)


def process_episode(model, episode_path: Path):
    files = sorted([path.as_posix() for path in episode_path.glob("*.png")])

    image = cv2.imread(files[0])
    image_height, image_width, num_channels = image.shape

    # take the spectograms apart into slices to be fed to the model
    slice_width = image_width // num_slices
    model_in = np.empty(
        (
            len(files),
            num_slices,
            image_height,
            slice_width,
            num_channels,
        )
    )

    for file_idx, file in enumerate(files):
        image = cv2.imread(file)
        for slice_idx in range(num_slices):
            model_in[file_idx, slice_idx] = image[
                :, slice_idx * slice_width : (slice_idx + 1) * slice_width
            ]

    # make predictions
    out_pred = model.predict(model_in, batch_size=1)
    del model_in

    # merge prediction into one time series
    flat_pred = out_pred.reshape(np.prod(out_pred.shape[:2]), out_pred.shape[2])

    # prepare output
    pred = np.argmax(flat_pred, axis=1)

    # merge segments of only 1 slice into previous segment
    for j in range(1, len(pred) - 1):
        if pred[j] != pred[j - 1] and pred[j] != pred[j + 1]:
            pred[j] = pred[j - 1]

    np.savez_compressed(f"{episode_path.name}.npz", pred)


if __name__ == "__main__":
    model = keras.models.load_model(Path(__file__).parent / "model.h5", compile=False)
    episode_paths = [path for path in Path("zcrgrams").iterdir() if path.is_dir()]
    for episode_path in tqdm(episode_paths):
        process_episode(model, episode_path)
