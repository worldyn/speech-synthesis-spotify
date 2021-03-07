from pathlib import Path
import json
import numpy as np
from tqdm import tqdm


def process_episode(annotation_path: Path):
    with np.load(annotation_path) as annotation_file:
        predictions = annotation_file["arr_0"]

    allowed_classes = [1, 2]
    predictions_expanded = [0] + list(predictions) + [0]
    pairs = list(enumerate(zip(predictions_expanded[:-1], predictions_expanded[1:])))
    starts = [
        idx
        for idx, (prev_prediction, next_prediction) in pairs
        if prev_prediction not in allowed_classes and next_prediction in allowed_classes
    ]
    ends = [
        idx
        for idx, (prev_prediction, next_prediction) in pairs
        if prev_prediction in allowed_classes and next_prediction not in allowed_classes
    ]
    segments = list(zip(starts, ends))

    with open(annotation_path.name.replace("npz", "json"), "w") as file:
        json.dump(indices_to_seconds(segments), file)


def indices_to_seconds(arr):
    arr = np.array(arr) * 0.05
    return arr.tolist()


if __name__ == "__main__":
    annotation_paths = list(Path("./breath").glob("*.npz"))
    for annotation_path in tqdm(annotation_paths):
        process_episode(annotation_path)
