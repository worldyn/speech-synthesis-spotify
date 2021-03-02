from os import stat
import scipy.io.wavfile
import numpy as np
import json
import sys
import pickle

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



# Creating a sample input file
'''
obj = (['smaller7tmono.wav'],[[(0.0, 5.5), (8.2, 15.7), (17.2, 19)]])

pickle.dump(obj, open('data.in', 'wb'))
'''

# Constants
OUTPUT_FILENAME = 'merged.out'

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


for ep_id, ep_timestamps in enumerate(timestamps):
    for segment_timestamps in ep_timestamps:
        ep_path = paths[ep_id]
        



# For future help

def count_speakers_and_time(path):
    speaker_tags = {1} # set of speakers
    time_length = 0
    with open(path) as f:
        data = json.load(f)
    for alt in data['results']:
        for a_dict in alt['alternatives']:
            try:
                words = a_dict['words']
            except:
                continue
            for word_dict in words:
                # either all words contain speakerTag or none does
                time_length = max(float(word_dict['endTime'][:-1]), time_length)
                try:
                    speaker = word_dict['speakerTag']
                    speaker_tags.add(speaker) # constant time compl 
                except:
                    break
    return len(speaker_tags), time_length

