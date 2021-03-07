import numpy as np
import json
import ntpath
import os
from scipy.io import wavfile
import parselmouth
#from utilsfilter import *
from g2p_en import G2p

'''
## Features of interest
    - Pitch
    - F0
    - Speech Rate
    - Energy
    - Intensity
    - Length

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

# Uses the parselmouth library for audio data usage
# https://parselmouth.readthedocs.io

class Segment:
    # todo extract parts
    def __init__(self, path, start_time, end_time, samp_freq = 44100, text=''):
        self.path = path # episode path
        self.start_time = start_time
        self.end_time = end_time
        self.time = end_time - start_time
        snd = parselmouth.Sound(path)
        self.snd = snd.extract_part(
            from_time = start_time,
            to_time = end_time
        )
        self.data = self.snd.values.T # amplitudes
        print("LEN",len(self.data))

        self.samp_freq = samp_freq
        #self.spectrogram = self.snd.to_spectrogram()
        self.intensity = self.snd.to_intensity()
        self.pitch_obj = self.snd.to_pitch()
        self.pitch = self.pitch_obj.selected_array['frequency']
        self.energy = self.snd.get_energy()

        self.text = text

    def write(self,path): 
       wavfile.write(path, self.samp_freq, self.data) 

    def pitch_avg(self):
        return np.average(self.pitch)

    def get_energy(self):
        return self.energy

    def intensity_avg(self):
        return np.average(self.intensity)
    
    def get_speech_rate(self):
        # Uses g2pE for phoneme conversion
        # https://github.com/Kyubyong/g2p
        g2p = G2p()
        phonemes = g2p(self.text)
        phonemes = [s for s in phonemes if s.strip()]
        return len(phonemes) / self.time


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
            #print(ep_timestamps, ep_transcripts)
            seg_start = ep_timestamps[j][0]
            seg_end = ep_timestamps[j][1]
            transcript = ep_transcripts[j]
            seg = Segment(
                DATA_PATH + ep_path, 
                seg_start, 
                seg_end, 
                text=transcript
            )
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
        'avg_length' : [],
        'std_f0': [],
        'std_pitch': [],
        'std_sr': [],
        'std_energy': [],
        'std_intensity': [],
        'std_length': []
    }

    show_stats = {
        'avg_f0': 0,
        'avg_pitch': 0,
        'avg_sr': 0,
        'avg_energy': 0,
        'avg_intensity': 0,
        'avg_length' : 0,
        'std_f0': 0,
        'std_pitch': 0,
        'std_sr': 0,
        'std_energy': 0,
        'std_intensity': 0,
        'std_length': 0
    }

    show_avg_f0 = []
    show_avg_pitch = []
    show_avg_sr = []
    show_avg_energy = []
    show_avg_intensity = []
    show_avg_length = []
    for ep_segments in show_segments:
        ep_avg_f0 = []
        ep_avg_pitch = []
        ep_avg_sr = []
        ep_avg_energy = []
        ep_avg_intensity = []
        ep_avg_length = []
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
            # Length
            length = segment.time
            ep_avg_length.append(length)
            show_avg_length.append(length)

        ep_stats['avg_f0'].append(np.mean(ep_avg_f0))
        ep_stats['avg_pitch'].append(np.mean(ep_avg_pitch))
        ep_stats['avg_sr'].append(np.mean(ep_avg_sr))
        ep_stats['avg_energy'].append(np.mean(ep_avg_energy))
        ep_stats['avg_intensity'].append(np.mean(ep_avg_intensity))
        ep_stats['avg_length'].append(np.mean(ep_avg_length))

        ep_stats['std_f0'].append(np.std(ep_avg_f0))
        ep_stats['std_pitch'].append(np.std(ep_avg_pitch))
        ep_stats['std_sr'].append(np.std(ep_avg_sr))
        ep_stats['std_energy'].append(np.std(ep_avg_energy))
        ep_stats['std_intensity'].append(np.std(ep_avg_intensity))
        ep_stats['std_length'].append(np.std(ep_avg_length))


    show_stats['avg_f0'] = np.mean(show_avg_f0)
    show_stats['avg_pitch'] = np.mean(show_avg_pitch)
    show_stats['avg_sr'] = np.mean(show_avg_sr)
    show_stats['avg_energy'] = np.mean(show_avg_energy)
    show_stats['avg_intensity'] = np.mean(show_avg_intensity)
    show_stats['avg_length'] = np.mean(show_avg_length)
    
    show_stats['std_f0'] = np.std(show_avg_f0)
    show_stats['std_pitch'] = np.std(show_avg_pitch)
    show_stats['std_sr'] = np.std(show_avg_sr)
    show_stats['std_energy'] = np.std(show_avg_energy)
    show_stats['std_intensity'] = np.std(show_avg_intensity)
    show_stats['std_length'] = np.std(show_avg_length)

    return show_stats, ep_stats

def filter_segments(show_segments, show_stats, ep_stats, filter_f0 = True, filter_pitch = True, filter_sr = True, filter_energy = True, filter_intensity = True, filter_length = True):
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
                'avg_length': ep_stats['avg_length'][ep_index],
                'std_f0': ep_stats['std_f0'][ep_index],
                'std_pitch': ep_stats['std_pitch'][ep_index],
                'std_sr': ep_stats['std_sr'][ep_index],
                'std_energy': ep_stats['std_energy'][ep_index],
                'std_intensity': ep_stats['std_intensity'][ep_index],
                'std_length': ep_stats['std_length'][ep_index]
            }

            if inside_intervals(segment=segment, stats=this_ep_stats, filter_f0=filter_f0, filter_pitch=filter_pitch, filter_sr=filter_sr, filter_energy=filter_energy, filter_intensity=filter_intensity, filter_length=filter_length):

                episode_level.append(segment)

            if inside_intervals(segment=segment, stats=show_stats, filter_f0=filter_f0, filter_pitch=filter_pitch, filter_sr=filter_sr, filter_energy=filter_energy, filter_intensity=filter_intensity, filter_length=filter_length):
                show_level.append(segment)

    return show_level, episode_level

def inside_intervals(segment, stats, filter_f0, filter_pitch, filter_sr, filter_energy, filter_intensity, filter_length):

    # F0
    ''''
    if filter_f0:
        lower_bound = stats['avg_f0'] - stats['std_f0']*F0_INTERVAL/2
        upper_bound = stats['avg_f0'] + stats['std_f0']*F0_INTERVAL/2
        
        f0 = segment.
        if f0 < lower_bound or f0 > upper_bound:
            return False 
    '''

    # Pitch
    if filter_pitch:
        lower_bound = stats['avg_pitch'] - stats['std_pitch']*PITCH_INTERVAL/2
        upper_bound = stats['avg_pitch'] + stats['std_pitch']*PITCH_INTERVAL/2
        
        pitch = segment.pitch_avg()
        if pitch < lower_bound or pitch > upper_bound:
            return False 

    # Speech Rate
    if filter_sr:
        lower_bound = stats['avg_sr'] - stats['std_sr']*SR_INTERVAL/2
        upper_bound = stats['avg_sr'] + stats['std_sr']*SR_INTERVAL/2
        
        sr = segment.get_speech_rate()
        if sr < lower_bound or sr > upper_bound:
            return False

    # Energy
    if filter_energy:
        lower_bound = stats['avg_energy'] - stats['std_energy']*ENERGY_INTERVAL/2
        upper_bound = stats['avg_energy'] + stats['std_energy']*ENERGY_INTERVAL/2
        
        energy = segment.get_energy()
        if energy < lower_bound or energy > upper_bound:
            return False 

    # Intensity
    if filter_intensity:
        lower_bound = stats['avg_intensity'] - stats['std_intensity']*INTENSITY_INTERVAL/2
        upper_bound = stats['avg_intensity'] + stats['std_intensity']*INTENSITY_INTERVAL/2
        
        intensity = segment.intensity_avg()
        if intensity < lower_bound or intensity > upper_bound:
            return False 

    # Length
    if filter_length:

        length = segment.time
        
        
        if length > LENGTH_TOP_BOUND or length < LENGTH_BOTTOM_BOUND:
            return False

        #lower_bound = stats['avg_length'] - stats['std_length']*intervals['intensity_length']/2
        #upper_bound = stats['avg_length'] + stats['std_length']*intervals['intensity_length']/2
        
        #if intensity < lower_bound or intensity > upper_bound:
        #    return False 

    return True

# Constants
INPUT_FILENAME = 'merged/merged.json'
SHOW_OUTPUT_FILENAME = 'filtered/filtered_show.json'
DATA_PATH = 'audio/'
EP_OUTPUT_FILENAME = 'filtered/filtered_ep.json'
SEGMENTS_KEPT_OUTDIR = 'filtered/'
#SEGMENTS_REMOVE_OUTDIR = 'segments_removed/'
FILTER_F0 = 1
FILTER_PITCH = 1
FILTER_SR = 1
FILTER_ENERGY = 1
FILTER_INTENSITY = 1
FILTER_LENGTH = 1

F0_INTERVAL = 1
PITCH_INTERVAL = 1
SR_INTERVAL = 1
ENERGY_INTERVAL = 1
INTENSITY_INTERVAL = 1
LENGTH_BOTTOM_BOUND = 3
LENGTH_TOP_BOUND = 10


def main():

    global F0_INTERVAL, PITCH_INTERVAL, SR_INTERVAL, ENERGY_INTERVAL, INTENSITY_INTERVAL, LENGTH_BOTTOM_BOUND, LENGTH_TOP_BOUND

    F0_INTERVAL = float(F0_INTERVAL)
    PITCH_INTERVAL = float(PITCH_INTERVAL)
    SR_INTERVAL = float(SR_INTERVAL)
    ENERGY_INTERVAL = float(ENERGY_INTERVAL)
    INTENSITY_INTERVAL = float(INTENSITY_INTERVAL)
    LENGTH_BOTTOM_BOUND = float(LENGTH_BOTTOM_BOUND)
    LENGTH_TOP_BOUND = float(LENGTH_TOP_BOUND)

    # check that correct dirs exist
    if not os.path.isdir(SEGMENTS_KEPT_OUTDIR):
        print("Directory ", SEGMENTS_KEPT_OUTDIR, " doesn't exist...")
    if not os.path.isdir(DATA_PATH):
        print(DATA_PATH, " directory doesn't exist...")

    '''
    # Loading the intervals from INTERVAL_FILE
    with open(INTERVAL_FILE) as file:
        intervals = json.load(file)

    print(intervals)
    '''

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

    #print(paths)
    #print(timestamps)
    #print(transcripts)

    assert len(paths) == len(timestamps)

    # Group the segments by episode
    paths, timestamps, transcripts = group_segments(paths=paths, timestamps=timestamps, transcripts=transcripts)
    #print(paths)
    #print(timestamps)
    #print(transcripts)

    # Creating a list of Segment objects
    show_segments = create_segments(paths=paths, timestamps=timestamps, transcripts=transcripts)
    #print(show_segments)

    # Computing episodes and show stats
    show_stats, ep_stats = compute_stats(show_segments=show_segments)
    #print('Show stats:', show_stats)
    #print('Episode stats:', show_stats)

    # Filtering the episodes

    show_level, episode_level = filter_segments(
        show_segments=show_segments, 
        show_stats=show_stats, 
        ep_stats=ep_stats, 
        filter_f0=FILTER_F0, 
        filter_pitch=FILTER_PITCH, 
        filter_sr=FILTER_SR, 
        filter_energy=FILTER_ENERGY, 
        filter_intensity=FILTER_INTENSITY,
        filter_length=FILTER_LENGTH
    )

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
    for i,segment in enumerate(episode_level):
        # save specific segment data instead of reference
        # to the whole episode
        ep_name_wav = ntpath.basename(segment.path)
        ep_name = os.path.splitext(ep_name_wav)[0]
        segment_saved_path = SEGMENTS_KEPT_OUTDIR + ep_name \
            + "_segment" + str(i) + ".wav"
        segment.write(segment_saved_path)
        paths.append(segment_saved_path)
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
 
