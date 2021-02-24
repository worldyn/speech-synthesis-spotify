from pathlib import Path
import numpy as np
import cv2

from .helpers import list_filenames, annot2textgrid


model_path = Path(__file__).parent / "model.h5"
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


# prepare the coloured spectrograms to take them through the model
files = list(list_filenames(output_root + "zcrgrams/" + output_prefix, [".png"]))
files.sort()
print("number of files:", len(files))

im = cv2.imread(files[0])
# x_complete is recreated from the saved spectrograms (saving and loading it
# changed the output)
x_complete = np.empty(
    (np.shape(files)[0], np.shape(im)[0], np.shape(im)[1], np.shape(im)[2])
)
for j in range(0, np.shape(files)[0]):
    x_complete[j, :, :, :] = cv2.imread(files[j])

# input image dimensions
img_rows, img_cols = np.shape(x_complete)[1], np.shape(x_complete)[2]

# take the spectogram apart into slices to be fed to the model
img_cols2 = img_cols // timesteps
print("frames per model input slice:", img_cols2)

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
print("model input shape:", np.shape(x2_pred))

# make predictions
model = keras.models.load_model(trained_model, compile=False)
out_pred = model.predict(x2_pred, batch_size=1)
print("prediction shape", np.shape(out_pred))

# merge prediction into one time series
flat_pred = np.empty(
    (np.shape(out_pred)[0] * np.shape(out_pred)[1], np.shape(out_pred)[2])
)
for j in range(0, np.shape(out_pred)[0]):
    flat_pred[j * timesteps : (j + 1) * timesteps, :] = out_pred[j, :, :]
print("flattened prediction shape:", np.shape(flat_pred))


# clean up and save results
if not os.path.exists(output_root + "predictions/"):
    os.makedirs(output_root + "predictions/")
np.save(output_root + "predictions/" + output_prefix + ".npy", flat_pred)
del out_pred, x2_pred, x_complete

# this code is a simplified version, providing no speaker separation
# the pretrained model is aimed at separating breath groups
#    two speaker labels: {0: noise/music, 1: breath s1, 2: breath s2, 3: silence,
#    4: speech s1, 5: speech s2, 6: segment with mixed speech}
#    NT single speaker original labels: {0: breath, 1: pause, 2: speech}
#    LV original labels: {0: breath, 1: speech, 2: noise}

try:
    flat_pred
except NameError:
    flat_pred = np.load(output_root + "predictions/" + output_prefix + ".npy")
# flat_pred = np.load(output_root + 'predictions/ep' + episode + '.npy')

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

# create annotation textgrid
filename = data_root + output_prefix
labels = ["n", "b", "na", "sil", "sp"]

annot2textgrid(filename, labels, pred, timesteps=40)
