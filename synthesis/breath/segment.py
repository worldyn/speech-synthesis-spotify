from pathlib import Path
import json
import numpy as np
from tqdm import tqdm


def process_episode(annotation_path: Path):
    with np.load(annotation_path) as annotation_file:
        arr = annotation_file["arr_0"]
    start = -2
    end = -1
    result_arr = []

    for index, a in enumerate(arr):
        if a == 1:
            if arr[index - 1] != 1 or index == 0:
                start = index
            if index == len(arr) - 1 or arr[index + 1] != 1:
                end = index
                result_arr.append([start, end])

    with open(annotation_path.name.replace("npz", "json"), "w") as file:
        json.dump(trans_in_seconds(result_arr), file)


def trans_in_seconds(arr):
    arr = np.array(arr) * 0.05
    return arr.tolist()


if __name__ == "__main__":
    annotation_paths = list(Path("./breath").glob("*.npz"))
    for annotation_path in tqdm(annotation_paths):
        process_episode(annotation_path)
