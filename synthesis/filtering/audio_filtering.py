from os import stat
import scipy.io.wavfile
import numpy as np
import json
import sys
import pickle
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

def compute_stats(show_segments):

    ep_stats = {
        'avg_f0': [],
        'avg_pitch': [],
        'avg_sr': [],
        'avg_energy': [],
        'avg_intensity': []
    }

    show_stats = {
        'avg_f0': 0,
        'avg_pitch': 0,
        'avg_sr': 0,
        'avg_energy': 0,
        'avg_intensity': 0
    }

    n_total_segments = 0
    show_avg_f0 = show_avg_pitch = show_avg_sr = show_avg_energy = show_avg_intensity = 0
    for ep_segments in show_segments:
        ep_avg_f0 = ep_avg_pitch = ep_avg_sr = ep_avg_energy = ep_avg_intensity = 0
        for segment in ep_segments:
            # F0
            #f0 = segment.
            #ep_avg_f0 += f0
            #show_avg_f0 += f0 
            # Pitch
            pitch = segment.pitch_avg()
            ep_avg_pitch += pitch
            show_avg_pitch += pitch
            # Speech Rate
            #sr = segment.get_speech_rate()
            #ep_avg_sr += sr
            #show_avg_sr += sr
            # Energy
            energy = segment.get_energy()
            ep_avg_energy += energy
            show_avg_energy += energy
            # Intensity 
            intensity = segment.intensity_avg()
            ep_avg_intensity += intensity
            show_avg_intensity += intensity

            n_total_segments += 1

        n_ep_segments = len(ep_segments)
        ep_avg_f0 /= n_ep_segments
        ep_avg_pitch /= n_ep_segments
        ep_avg_sr /= n_ep_segments
        ep_avg_energy /= n_ep_segments
        ep_avg_intensity /= n_ep_segments

        ep_stats['avg_f0'].append(ep_avg_f0)
        ep_stats['avg_pitch'].append(ep_avg_pitch)
        ep_stats['avg_sr'].append(ep_avg_sr)
        ep_stats['avg_energy'].append(ep_avg_energy)
        ep_stats['avg_intensity'].append(ep_avg_intensity)


    show_avg_f0 /= n_total_segments
    show_avg_pitch /= n_total_segments
    show_avg_sr /= n_total_segments
    show_avg_energy /= n_total_segments
    show_avg_intensity /= n_total_segments

    show_stats['avg_f0'] = show_avg_f0
    show_stats['avg_pitch'] = show_avg_pitch
    show_stats['avg_sr'] = show_avg_sr
    show_stats['avg_energy'] = show_avg_energy
    show_stats['avg_intensity'] = show_avg_intensity

    return show_stats, ep_stats

def inside_intervals(segment, stats, intervals):

    # F0
    ''''
    lower_bound = stats['avg_f0'] - stats['avg_f0']*intervals['f0_interval']/2
    upper_bound = stats['avg_f0'] + stats['avg_f0']*intervals['f0_interval']/2
    
    f0 = segment.
    if f0 < lower_bound or f0 > upper_bound:
        return False 
    '''

    # Pitch
    lower_bound = stats['avg_pitch'] - stats['avg_pitch']*intervals['pitch_interval']/2
    upper_bound = stats['avg_pitch'] + stats['avg_pitch']*intervals['pitch_interval']/2
    
    pitch = segment.pitch_avg()
    if pitch < lower_bound or pitch > upper_bound:
        return False 

    # Speech Rate
    '''
    lower_bound = stats['avg_sr'] - stats['avg_sr']*intervals['sr_interval']/2
    upper_bound = stats['avg_sr'] + stats['avg_sr']*intervals['sr_interval']/2
    
    sr = segment.get_speech_rate()
    if sr < lower_bound or sr > upper_bound:
        return False
    '''

    # Energy
    lower_bound = stats['avg_energy'] - stats['avg_energy']*intervals['energy_interval']/2
    upper_bound = stats['avg_energy'] + stats['avg_energy']*intervals['energy_interval']/2
    
    energy = segment.get_energy()
    if energy < lower_bound or energy > upper_bound:
        return False 

    # Intensity
    lower_bound = stats['avg_intensity'] - stats['avg_intensity']*intervals['intensity_interval']/2
    upper_bound = stats['avg_intensity'] + stats['avg_intensity']*intervals['intensity_interval']/2
    
    intensity = segment.intensity_avg()
    if intensity < lower_bound or intensity > upper_bound:
        return False 

    return True

# Creating the intervals file
'''
intervals = {
    "f0_interval": 0.8,
    "pitch_interval": 0.5,
    "sr_interval": 0.2,
    "energy_interval": 0.5,
    "intensity_interval": 0.3
}

with open('intervals.json', 'w') as file:
    json.dump(intervals, file, indent=4)

'''

# Creating a sample input file
'''
obj = (['smaller7tmono.wav'],[[(0.0, 5.5), (8.2, 15.7), (17.2, 19)]])

pickle.dump(obj, open('data.in', 'wb'))
'''

# Constants
INTERVAL_FILE = 'intervals.json'
SHOW_OUTPUT_FILENAME = 'filtered_show.out'
EP_OUTPUT_FILENAME = 'filtered_ep.out'

# Loading the intervals from INTERVAL_FILE
with open(INTERVAL_FILE) as file:
    intervals = json.load(file)

print(intervals)

# Loading the data

params = arg_parse(sys.argv)

input_filename = params['input_filename']

with open(input_filename, 'rb') as file:
    file = pickle.load(file)
    paths = file[0]
    timestamps = file[1]

print(paths)
print(timestamps)

assert len(paths) == len(timestamps)

# Creating a list of Segment objects
show_segments = []
for i in range(len(paths)):
    ep_path = paths[i]
    ep_timestamps = timestamps[i]
    ep_segments = []
    for seg_start, seg_end in ep_timestamps:
        seg = Segment(ep_path, seg_start, seg_end)
        ep_segments.append(seg)
    show_segments.append(ep_segments)

print(show_segments)

# Computing episodes and show stats
show_stats, ep_stats = compute_stats(show_segments=show_segments)
print('Show stats:', show_stats)
print('Episode stats:', show_stats)

# Filtering the episodes

show_level = []
episode_level = []

for ep_index, ep_segments in enumerate(show_segments):
    for segment in ep_segments:
        this_ep_stats = {
            'avg_f0': ep_stats['avg_f0'][ep_index],
            'avg_pitch': ep_stats['avg_pitch'][ep_index],
            'avg_sr': ep_stats['avg_sr'][ep_index],
            'avg_energy': ep_stats['avg_energy'][ep_index],
            'avg_intensity': ep_stats['avg_intensity'][ep_index]
        }

        if inside_intervals(segment=segment, stats=this_ep_stats, intervals=intervals):
            episode_level.append(segment)

        if inside_intervals(segment=segment, stats=show_stats, intervals=intervals):
            show_level.append(segment)

print(len(show_level), 'segments kept at show level')
print(len(episode_level), 'segments kept at episode level')

# Storing show level

paths = []
timestamps = []
for segment in show_level:
    paths.append(segment.path)
    timestamps.append((segment.start_time, segment.end_time))

with open(SHOW_OUTPUT_FILENAME, 'wb') as file:
    pickle.dump((paths, timestamps), file)

# Storing episode level

paths = []
timestamps = []
for segment in episode_level:
    paths.append(segment.path)
    timestamps.append((segment.start_time, segment.end_time))

with open(EP_OUTPUT_FILENAME, 'wb') as file:
    pickle.dump((paths, timestamps), file)



 



