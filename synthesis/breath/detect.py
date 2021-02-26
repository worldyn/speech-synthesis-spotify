from pathlib import Path
import numpy as np
import cv2
import keras
from tqdm.auto import tqdm

from .helpers import annot2textgrid


nr_speakers = 1  # pretrained model is single speaker

# output settings
n_mels = 128
timesteps = 40  # timesteps in keras model, standard 2 seconds with 20 steps each
slicepersec = 400

# corpus creation settings
max_utt = 12  # maximum utterance length (seconds)
min_utt = 1.0  # minimum utterance length (seconds)
trail = 0.02  # silence before and after utterance (seconds)
trailfr = 0  # additional frame(s) included for smoother end of utterance (1 for TCC / 0 for Obama)


def process_episode(episode_path: Path):
    print("Begin processing episode " + episode_path.name)

    files = sorted(episode_path.glob("*.png"))
    print(f"Number of zcrgrams in episode: {len(files)}")

    im = cv2.imread(files[0])
    x_complete = np.empty(
        (np.shape(files)[0], np.shape(im)[0], np.shape(im)[1], np.shape(im)[2])
    )
    for j in range(0, np.shape(files)[0]):
        x_complete[j, :, :, :] = cv2.imread(files[j])

    # input image dimensions
    img_rows, img_cols = np.shape(x_complete)[1], np.shape(x_complete)[2]

    # take the spectogram apart into slices to be fed to the model
    img_cols2 = img_cols // timesteps
    print(f"Frames per model input slice: {img_cols2}")

    x2_pred = np.empty(
        (
            np.shape(x_complete)[0],
            timesteps,
            np.shape(x_complete)[1],
            img_cols2,
            np.shape(x_complete)[3],
        )
    )

    for j in range(0, np.shape(x_complete)[0]):
        for k in range(0, timesteps):
            x2_pred[j, k, :, :, :] = x_complete[
                j, :, k * img_cols2 : (k + 1) * img_cols2, :
            ]
    print("Model input shape:", np.shape(x2_pred))

    # make predictions
    model = keras.models.load_model(Path(__file__).parent / "model.h5", compile=False)
    out_pred = model.predict(x2_pred, batch_size=1)
    print("Prediction shape", np.shape(out_pred))

    # merge prediction into one time series
    flat_pred = np.empty(
        (np.shape(out_pred)[0] * np.shape(out_pred)[1], np.shape(out_pred)[2])
    )
    for j in range(0, np.shape(out_pred)[0]):
        flat_pred[j * timesteps : (j + 1) * timesteps, :] = out_pred[j, :, :]
    print("Flattened prediction shape:", np.shape(flat_pred))

    # this code is a simplified version, providing no speaker separation
    # the pretrained model is aimed at separating breath groups
    #    two speaker labels: {0: noise/music, 1: breath s1, 2: breath s2, 3: silence,
    #    4: speech s1, 5: speech s2, 6: segment with mixed speech}
    #    NT single speaker original labels: {0: breath, 1: pause, 2: speech}
    #    LV original labels: {0: breath, 1: speech, 2: noise}

    #    prepare output
    pred = np.argmax(flat_pred, axis=1)
    # merge segments of only 1 slice into previous segment
    for j in range(1, len(pred) - 1):
        if pred[j] != pred[j - 1] and pred[j] != pred[j + 1]:
            pred[j] = pred[j - 1]

    # align single speaker labelling to two speaker case
    if nr_speakers == 1:
        pred[pred == 1] = 4  # speech
        pred[pred == 0] = 1  # breath
        pred[pred == 2] = 0  # noise

    w_change = np.where(pred[:-1] != pred[1:])[0] + 1
    w_id = pred[w_change]  # identify changes in segment (breath, speech, speaker)
    w_br = np.where(np.logical_or(w_id == 1, w_id == 2))
    w_br = np.where((w_id == 1) | (w_id == 2))[0]  # identify breaths 2 speakers

    annot2textgrid(
        filename=episode_path.name + ".txt",
        labels=["n", "b", "na", "sil", "sp"],
        anoot=pred,
        timesteps=40,
    )


if __name__ == "__main__":
    episode_paths = [path for path in Path("zcrgrams").iterdir() if path.isdir()]
    for episode_path in tqdm(episode_paths):
        process_episode(episode_path)
