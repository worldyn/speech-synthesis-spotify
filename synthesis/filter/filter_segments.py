from typing import List, Tuple, Dict, Set
import numpy as np
import json
import ntpath
import os
from tqdm.auto import tqdm
from .segment import Segment


def group_segments(paths, timestamps, transcripts):
    ts = {}
    tr = {}
    for i in range(len(paths)):
        ts[paths[i]] = ts.get(paths[i], []) + [timestamps[i]]
        tr[paths[i]] = tr.get(paths[i], []) + [transcripts[i]]

    paths = []
    timestamps = []
    transcripts = []
    for k in ts.keys():
        paths.append(k.split("/")[-1])
        timestamps.append(ts[k])
        transcripts.append(tr[k])

    return paths, timestamps, transcripts


def create_segments(paths, timestamps, transcripts):
    show_segments = []
    for i in range(len(paths)):
        if i % 100 == 0:
            print("=> ", i, " / ", len(paths), " segments obj created...")
        ep_path = paths[i]
        ep_timestamps = timestamps[i]
        ep_transcripts = transcripts[i]
        ep_segments = []
        for j in range(len(ep_timestamps)):
            seg_start = ep_timestamps[j][0]
            seg_end = ep_timestamps[j][1]
            transcript = ep_transcripts[j]
            seg = Segment(DATA_PATH + ep_path, seg_start, seg_end, text=transcript)
            ep_segments.append(seg)
        show_segments.append(ep_segments)

    print("=> All objects created...")
    return show_segments


def filter_segments(
    show_segments: List[Segment],
    duration_range: Tuple[float],
    cut_fractions: Dict[str, float],
):
    fitting_duration = [
        [
            segment
            for segment in episode_segments
            if duration_range[0] <= segment.duration <= duration_range[1]
        ]
        for episode_segments in show_segments
    ]
    filtered_per_episode = set.union(
        *[
            filter_flat(episode_segments, cut_fractions)
            for episode_segments in fitting_duration
        ]
    )
    filtered_per_show = filter_flat(
        [
            segment
            for episode_segments in fitting_duration
            for segment in episode_segments
        ],
        cut_fractions,
    )
    return set.intersection(filtered_per_episode, filtered_per_show)


def filter_flat(segments: List[Segment], cut_fractions: Dict[str, float]):
    def filter_by(stat_name: str):
        num_cut = int(cut_fractions[stat_name] * len(segments) / 2)
        sorted_segments = sorted(
            segments, key=lambda segment: getattr(segment, stat_name)
        )
        return set(sorted_segments[num_cut : len(sorted_segments) - num_cut])

    return set.intersection(
        *[filter_by(stat_name) for stat_name in cut_fractions.keys()]
    )


# Constants
INPUT_FILENAME = "merged/merged.json"
SHOW_OUTPUT_FILENAME = "filtered_show.json"
DATA_PATH = "audio/"
EP_OUTPUT_FILENAME = "filtered_ep.json"

cutoff_pitch = 0.1
cutoff_energy = 0.1
cutoff_intensity = 0.1
cutoff_speech_rate = 0.1

min_duration = 3.0
max_duration = 10.0


def main():
    with open(INPUT_FILENAME) as file:
        data = json.load(file)

        paths = data["paths"]
        timestamps = data["timestamps"]

        try:
            transcripts = data["transcripts"]
        except:
            transcripts = [""] * len(paths)

    assert len(paths) == len(timestamps)

    print("=> Grouping segments by episode...")
    paths, timestamps, transcripts = group_segments(
        paths=paths, timestamps=timestamps, transcripts=transcripts
    )

    print("=> Creating segment objects...")
    show_segments = create_segments(
        paths=paths, timestamps=timestamps, transcripts=transcripts
    )
    print("=> Number of segment objects: ", len(show_segments))

    print("=> Filtering by stats...")
    kept_shows = filter_segments(
        show_segments=show_segments,
        duration_range=(min_duration, max_duration),
        cut_fractions=dict(
            pitch=cutoff_pitch,
            energy=cutoff_energy,
            intensity=cutoff_intensity,
            speech_rate=cutoff_speech_rate,
        ),
    )
    print(f"=> Will keep {len(kept_shows)} segments")

    paths = []
    timestamps = []
    transcripts = []
    for i, segment in tqdm(enumerate(kept_shows), desc="Storing segments"):
        ep_name_wav = ntpath.basename(segment.path)
        ep_name = os.path.splitext(ep_name_wav)[0]
        segment_saved_path = f"{ep_name}_segment_{i}.wav"
        segment.write(segment_saved_path)
        paths.append(segment_saved_path)
        timestamps.append((segment.start_time, segment.end_time))
        transcripts.append(segment.text)

    obj = {"paths": paths, "timestamps": timestamps, "transcripts": transcripts}

    with open(SHOW_OUTPUT_FILENAME, "w") as file:
        json.dump(obj, file, indent=4)


if __name__ == "__main__":
    main()
