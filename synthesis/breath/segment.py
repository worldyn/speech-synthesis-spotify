from pathlib import Path
import json
import numpy as np
from tqdm import tqdm


target_segment_seconds = 10
max_empty_seconds = 1


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
    segments_seconds = (np.array(segments) * 0.05).tolist()

    joined_segments = []
    for segment in segments_seconds:
        if len(joined_segments) == 0:
            joined_segments.append(segment)
            continue
        if (
            segment[1] - joined_segments[-1][0] < target_segment_seconds
            and segment[0] - joined_segments[-1][1] < max_empty_seconds
        ):
            joined_segments[-1][1] = segment[1]
        else:
            joined_segments.append(segment)

    with open(annotation_path.name.replace("npz", "json"), "w") as file:
        json.dump(joined_segments, file)


if __name__ == "__main__":
    annotation_paths = list(Path("./breath").glob("*.npz"))
    for annotation_path in tqdm(annotation_paths):
        process_episode(annotation_path)
