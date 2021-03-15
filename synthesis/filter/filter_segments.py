from typing import List, Tuple, Dict, Set
from pathlib import Path
import numpy as np
import json
import ntpath
import os
from tqdm.auto import tqdm
from .segment import Segment


cutoff_pitch = 0.1
cutoff_energy = 0.1
cutoff_intensity = 0.1
cutoff_speech_rate = 0.1

min_duration = 3.0
max_duration = 10.0


def main():
    with open("merged/merged.json") as file:
        data = json.load(file)

    segments = create_segments(data)
    kept_segments = filter_segments(
        segments=segments,
        duration_range=(min_duration, max_duration),
        cut_fractions=dict(
            pitch=cutoff_pitch,
            energy=cutoff_energy,
            intensity=cutoff_intensity,
            speech_rate=cutoff_speech_rate,
        ),
    )

    paths = []
    timestamps = []
    transcripts = []
    for i, segment in enumerate(tqdm(kept_segments, desc="Storing segments")):
        ep_name_wav = ntpath.basename(segment.path)
        ep_name = os.path.splitext(ep_name_wav)[0]
        segment_saved_path = f"{ep_name}_segment_{i}.wav"
        segment.write(segment_saved_path)
        paths.append(segment_saved_path)
        timestamps.append((segment.start_time, segment.end_time))
        transcripts.append(segment.text)

    with open("filtered.json", "w") as file:
        json.dump(
            {"paths": paths, "timestamps": timestamps, "transcripts": transcripts},
            file,
            indent=4,
        )


def create_segments(data):
    data_transposed = sorted(
        [
            (path, times, transcript)
            for path, times, transcript in zip(
                data["paths"], data["timestamps"], data["transcripts"]
            )
        ],
        key=lambda info: info[0],
    )  # sort by path to help caching
    return [
        Segment(
            path=(Path("audio") / path.split("/")[-1]).as_posix(),
            start_time=times[0],
            end_time=times[1],
            text=transcript,
        )
        for path, times, transcript in tqdm(
            data_transposed,
            desc="Creating segment objects",
        )
    ]


def filter_segments(
    segments: List[Segment],
    duration_range: Tuple[float],
    cut_fractions: Dict[str, float],
):
    fitting_duration = [
        segment
        for segment in segments
        if duration_range[0] <= segment.duration <= duration_range[1]
    ]
    filtered_per_episode = set.union(
        *[
            filter_flat(
                [
                    segment
                    for segment in fitting_duration
                    if segment.path == episode_path
                ],
                cut_fractions,
            )
            for episode_path in set(segment.path for segment in fitting_duration)
        ]
    )
    filtered_per_show = filter_flat(
        fitting_duration,
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


if __name__ == "__main__":
    main()
