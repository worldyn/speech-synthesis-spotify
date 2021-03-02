import numpy as np
import json
from segment import Segment

'''
## Features of interest
    - Pitch
    - F0
    - Speech Rate
    - Energy
    - Intensity

## Input:
    List of paths and list of lists of tuple timestamps in which the audio should be segmented
    - Path Type: [Paths],
    - Timestamps Type: [[(Ts0, Ts1), ...], [(Ts0, Ts1), ...], ...]

## Filtering

    1. Define constant confidence intervals for each feature: Dictionary
    Ex: 80% for Avg Pith, 50% for Energy

    2. Compute the avg value of each feature for Episode
        - If Sound.feature out of the interval [Avg feature - %, Avg feature + %]:
        Discard
        - Else
        Keep the segment:
        Store a list of tuples (init timestamp, final timestamp)

## Output

List of `Segments` representing valid segments
'''

def arg_parse(args):
    '''
    input: list of arguments
    output: dictionary with the parameters
    '''

    usage = 'python audio_filtering.py [input_file]'

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

def compute_stats(show_segments):

    ep_stats = {
        'avg_f0': [],
        'avg_pitch': [],
        'avg_sr': [],
        'avg_energy': [],
        'avg_intensity': [],
        'std_f0': [],
        'std_pitch': [],
        'std_sr': [],
        'std_energy': [],
        'std_intensity': []
    }

    show_stats = {
        'avg_f0': 0,
        'avg_pitch': 0,
        'avg_sr': 0,
        'avg_energy': 0,
        'avg_intensity': 0,
        'std_f0': 0,
        'std_pitch': 0,
        'std_sr': 0,
        'std_energy': 0,
        'std_intensity': 0
    }

    show_avg_f0 = []
    show_avg_pitch = []
    show_avg_sr = []
    show_avg_energy = []
    show_avg_intensity = []
    for ep_segments in show_segments:
        ep_avg_f0 = []
        ep_avg_pitch = []
        ep_avg_sr = []
        ep_avg_energy = []
        ep_avg_intensity = []
        for segment in ep_segments:
            # F0
            #f0 = segment.
            #ep_avg_f0.append(f0)
            #show_avg_f0.append(f0 )
            # Pitch
            pitch = segment.pitch_avg()
            ep_avg_pitch.append(pitch)
            show_avg_pitch.append(pitch)
            # Speech Rate
            sr = segment.get_speech_rate()
            ep_avg_sr.append(sr)
            show_avg_sr.append(sr)
            # Energy
            energy = segment.get_energy()
            ep_avg_energy.append(energy)
            show_avg_energy.append(energy)
            # Intensity 
            intensity = segment.intensity_avg()
            ep_avg_intensity.append(intensity)
            show_avg_intensity.append(intensity)


        ep_stats['avg_f0'].append(np.mean(ep_avg_f0))
        ep_stats['avg_pitch'].append(np.mean(ep_avg_pitch))
        ep_stats['avg_sr'].append(np.mean(ep_avg_sr))
        ep_stats['avg_energy'].append(np.mean(ep_avg_energy))
        ep_stats['avg_intensity'].append(np.mean(ep_avg_intensity))

        ep_stats['std_f0'].append(np.std(ep_avg_f0))
        ep_stats['std_pitch'].append(np.std(ep_avg_pitch))
        ep_stats['std_sr'].append(np.std(ep_avg_sr))
        ep_stats['std_energy'].append(np.std(ep_avg_energy))
        ep_stats['std_intensity'].append(np.std(ep_avg_intensity))


    show_stats['avg_f0'] = np.mean(show_avg_f0)
    show_stats['avg_pitch'] = np.mean(show_avg_pitch)
    show_stats['avg_sr'] = np.mean(show_avg_sr)
    show_stats['avg_energy'] = np.mean(show_avg_energy)
    show_stats['avg_intensity'] = np.mean(show_avg_intensity)
    
    show_stats['std_f0'] = np.std(show_avg_f0)
    show_stats['std_pitch'] = np.std(show_avg_pitch)
    show_stats['std_sr'] = np.std(show_avg_sr)
    show_stats['std_energy'] = np.std(show_avg_energy)
    show_stats['std_intensity'] = np.std(show_avg_intensity)

    return show_stats, ep_stats

def filter_segments(show_segments, show_stats, ep_stats, intervals, filter_f0 = True, filter_pitch = True, filter_sr = True, filter_energy = True, filter_intensity = True):
    show_level = []
    episode_level = []

    for ep_index, ep_segments in enumerate(show_segments):
        for segment in ep_segments:
            this_ep_stats = {
                'avg_f0': ep_stats['avg_f0'][ep_index],
                'avg_pitch': ep_stats['avg_pitch'][ep_index],
                'avg_sr': ep_stats['avg_sr'][ep_index],
                'avg_energy': ep_stats['avg_energy'][ep_index],
                'avg_intensity': ep_stats['avg_intensity'][ep_index],
                'std_f0': ep_stats['std_f0'][ep_index],
                'std_pitch': ep_stats['std_pitch'][ep_index],
                'std_sr': ep_stats['std_sr'][ep_index],
                'std_energy': ep_stats['std_energy'][ep_index],
                'std_intensity': ep_stats['std_intensity'][ep_index]
                
            }

            if inside_intervals(segment=segment, stats=this_ep_stats, intervals=intervals, filter_f0=filter_f0, filter_pitch=filter_pitch, filter_sr=filter_sr, filter_energy=filter_energy, filter_intensity=filter_intensity):
                episode_level.append(segment)

            if inside_intervals(segment=segment, stats=show_stats, intervals=intervals, filter_f0=filter_f0, filter_pitch=filter_pitch, filter_sr=filter_sr, filter_energy=filter_energy, filter_intensity=filter_intensity):
                show_level.append(segment)

    return show_level, episode_level

def inside_intervals(segment, stats, intervals, filter_f0, filter_pitch, filter_sr, filter_energy, filter_intensity):

    # F0
    ''''
    if filter_f0:
        lower_bound = stats['avg_f0'] - stats['std_f0']*intervals['f0_interval']/2
        upper_bound = stats['avg_f0'] + stats['std_f0']*intervals['f0_interval']/2
        
        f0 = segment.
        if f0 < lower_bound or f0 > upper_bound:
            return False 
    '''

    # Pitch
    if filter_pitch:
        lower_bound = stats['avg_pitch'] - stats['std_pitch']*intervals['pitch_interval']/2
        upper_bound = stats['avg_pitch'] + stats['std_pitch']*intervals['pitch_interval']/2
        
        pitch = segment.pitch_avg()
        if pitch < lower_bound or pitch > upper_bound:
            return False 

    # Speech Rate
    if filter_sr:
        lower_bound = stats['avg_sr'] - stats['std_sr']*intervals['sr_interval']/2
        upper_bound = stats['avg_sr'] + stats['std_sr']*intervals['sr_interval']/2
        
        sr = segment.get_speech_rate()
        if sr < lower_bound or sr > upper_bound:
            return False

    # Energy
    if filter_energy:
        lower_bound = stats['avg_energy'] - stats['std_energy']*intervals['energy_interval']/2
        upper_bound = stats['avg_energy'] + stats['std_energy']*intervals['energy_interval']/2
        
        energy = segment.get_energy()
        if energy < lower_bound or energy > upper_bound:
            return False 

    # Intensity
    if filter_intensity:
        lower_bound = stats['avg_intensity'] - stats['std_intensity']*intervals['intensity_interval']/2
        upper_bound = stats['avg_intensity'] + stats['std_intensity']*intervals['intensity_interval']/2
        
        intensity = segment.intensity_avg()
        if intensity < lower_bound or intensity > upper_bound:
            return False 

    return True

# Constants
INTERVAL_FILE = 'intervals.json'
INPUT_FILENAME = 'merged.json'
SHOW_OUTPUT_FILENAME = 'filtered_show.json'
EP_OUTPUT_FILENAME = 'filtered_ep.json'
FILTER_F0 = 1
FILTER_PITCH = 1
FILTER_SR = 1
FILTER_ENERGY = 1
FILTER_INTENSITY = 1

def main():

    # Loading the intervals from INTERVAL_FILE
    with open(INTERVAL_FILE) as file:
        intervals = json.load(file)

    print(intervals)

    # Loading the data

    #params = arg_parse(sys.argv)

    #input_filename = params['input_filename']

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



if __name__ == '__main__':
    main()
 



