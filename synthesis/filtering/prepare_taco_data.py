import numpy as np
import json
from segment import Segment

def arg_parse(args):
    '''
    input: list of arguments
    output: dictionary with the parameters
    '''

    usage = 'python prepare_taco_data.py [input_file]'

    if len(args) < 2 or '-h' in args or '--help' in args:
        print('Usage:', usage)
        exit()

    params = {
        'input_filename': args[1]
    }

    return params

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
        paths.append(k)
        timestamps.append(ts[k])
        transcripts.append(tr[k])

    return paths, timestamps, transcripts

def create_segments(paths, timestamps, transcripts):
    show_segments = []
    for i in range(len(paths)):
        ep_path = paths[i]
        ep_timestamps = timestamps[i]
        ep_transcripts = transcripts[i]
        ep_segments = []
        for j in range(len(ep_timestamps)):
            print(ep_timestamps, ep_transcripts)
            seg_start = ep_timestamps[j][0]
            seg_end = ep_timestamps[j][1]
            transcript = ep_transcripts[j]
            seg = Segment(ep_path, seg_start, seg_end, text=transcript)
            ep_segments.append(seg)
        show_segments.append(ep_segments)

    return show_segments

# Constants
INPUT_FILENAME = 'filtered_ep.json'
TRAIN_OUTPUT = 'ljs_audio_text_train_filelist.txt'
VAL_OUTPUT = 'ljs_audio_text_val_filelist.txt'
TEST_OUTPUT = 'ljs_audio_text_test_filelist.txt'
TRAIN_PERCENT = 0.96
VAL_PERCENT = 0.04
TEST_PERCENT = 0

def main():

    # Loading the intervals from INTERVAL_FILE
    with open(INPUT_FILENAME) as file:
         segments = json.load(file)

    #print(segments)

    # Loading the data
    paths = segments["paths"]
    timestamps = segments["timestamps"]
    transcripts = segments["transcripts"]

    print(paths)
    '''
    with open(INPUT_FILENAME) as file:
        data = json.load(file)

        paths = data['paths']
        timestamps = data['timestamps']

        try:
            transcripts = data['transcripts']
        except:
            transcripts = [""] * len(paths)

    print(paths)
    print(timestamps)
    print(transcripts)

    assert len(paths) == len(timestamps)

    # Group the segments by episode
    paths, timestamps, transcripts = group_segments(paths=paths, timestamps=timestamps, transcripts=transcripts)
    print(paths)
    print(timestamps)
    print(transcripts)

    # Creating a list of Segment objects
    show_segments = create_segments(paths=paths, timestamps=timestamps, transcripts=transcripts)
    print(show_segments)

    # Computing episodes and show stats
    show_stats, ep_stats = compute_stats(show_segments=show_segments)
    print('Show stats:', show_stats)
    print('Episode stats:', show_stats)

    # Filtering the episodes

    show_level, episode_level = filter_segments(show_segments=show_segments, show_stats=show_stats, ep_stats=ep_stats, intervals=intervals, 
        filter_f0=FILTER_F0, filter_pitch=FILTER_PITCH, filter_sr=FILTER_SR, filter_energy=FILTER_ENERGY, filter_intensity=FILTER_INTENSITY)

    print(len(show_level), 'segments kept at show level')
    print(len(episode_level), 'segments kept at episode level')

    # Storing show level

    paths = []
    timestamps = []
    transcripts = []
    for segment in show_level:
        paths.append(segment.path)
        timestamps.append((segment.start_time, segment.end_time))
        transcripts.append(segment.text)

    obj = {
        'paths': paths,
        'timestamps': timestamps,
        'transcripts': transcripts
    }

    with open(SHOW_OUTPUT_FILENAME, 'w') as file:
        json.dump(obj, file, indent=4)

    # Storing episode level

    paths = []
    timestamps = []
    transcripts = []
    for segment in episode_level:
        paths.append(segment.path)
        timestamps.append((segment.start_time, segment.end_time))
        transcripts.append(segment.text)

    obj = {
        'paths': paths,
        'timestamps': timestamps,
        'transcripts': transcripts
    }

    with open(EP_OUTPUT_FILENAME, 'w') as file:
        json.dump(obj, file, indent=4)

'''


if __name__ == '__main__':
    main()
 



