from os import stat
import scipy.io.wavfile
import numpy as np
import json
import sys
import pickle


def group_segments(paths, timestamps):
    ts = {}
    for i in range(len(paths)):
        ts[paths[i]] = ts.get(paths[i], []) + [timestamps[i]]
        

    paths = []
    timestamps = []
    for k in ts.keys():
        paths.append(k)
        timestamps.append(ts[k])

    return paths, timestamps

def fill_show(paths, timestamps):
    
    transcripts = []
    for ep_path, ep_timestamps in zip(paths, timestamps):
        ep_transcripts = fill_episode(ep_path, ep_timestamps)
        transcripts.append(ep_transcripts)

    return transcripts


def fill_episode(ep_path, ep_timestamps):
    transcripts = [""] * len(ep_timestamps)
    ep_path = ep_path.replace('.wav', '.json')
    with open(ep_path) as f:
        data = json.load(f)

    for i, timestamp in enumerate(ep_timestamps):
        copy_next = False
        found = False
        for alt in data['results']:
            for a_dict in alt['alternatives']:
                try:
                    words = a_dict['words']
                except:
                    continue
                for word_dict in words:

                    if found and not copy_next:
                        continue

                    # Check if we have found the first word
                    text_end = float(word_dict['endTime'][:-1])
                    if text_end > timestamp[0] and not found:
                        found = True
                        copy_next = True

                    # Check if we should copy the word
                    if copy_next:
                        transcripts[i] += word_dict['word'] + ' '

                    # Check if we have found the last word
                    if text_end > timestamp[1] and copy_next:
                        copy_next = False
                        transcripts[i] = transcripts[i][:-1]
    
    print(transcripts)
    return transcripts

                    
                    

# Constants
INPUT_FILENAME = 'input_segments.json'
OUTPUT_FILENAME = 'merged.json'

def main():

    # Loading the data

    with open(INPUT_FILENAME) as file:
        data = json.load(file)

        paths = data['paths']
        timestamps = data['timestamps']

    assert len(paths) == len(timestamps)

    # Group the segments by episode
    paths, timestamps = group_segments(paths=paths, timestamps=timestamps)
    print(paths)
    print(timestamps)

    transcripts = fill_show(paths, timestamps)
            
    # Storing episode level

    paths_list = []
    timestamps_list = []
    transcripts_list = []
    for ep_path, ep_timestamps, ep_transcripts in zip(paths, timestamps, transcripts):
        for timestamp, transcript in zip (ep_timestamps, ep_transcripts):
            paths_list.append(ep_path)
            timestamps_list.append(timestamp)
            transcripts_list.append(transcript)

    obj = {
        'paths': paths_list,
        'timestamps': timestamps_list,
        'transcripts': transcripts_list
    }

    with open(OUTPUT_FILENAME, 'w') as file:
        json.dump(obj, file, indent=4)

if __name__ == '__main__':
    main()