import json
import os
# same speakerTag
LOCAL_PATH = "./data/spotify-podcasts-2020/podcasts-transcripts" # hardcoded


def collect_files():

    valid_shows = []

    for subdir, dirs, files in os.walk(LOCAL_PATH):
        for filename in files:

            if '.ogg' in filename or '.wav' in filename:
                continue

            subdir = subdir.replace('\\', '/')

            res = valid_1_speaker(subdir)

            if res and res[0]:
                valid_shows.append(subdir)

            break

    
    return valid_shows


# return Valid_episodes and total_show_time if the show is valid, False otherwise 
def valid_1_speaker(show_dir):

    print(show_dir)

    valid_episodes = []
    total_show_time = 0

    for subdir, dirs, files in os.walk(show_dir):
        for filename in files:

            if '.ogg' in filename or '.wav' in filename:
                continue

            path = show_dir + '/' + filename

            n_speakers, ep_time = count_speakers_and_time(path)

            if n_speakers == 1:
                valid_episodes.append(filename)
            
            total_show_time += ep_time

    hours = 20
    if total_show_time < hours*60*60:
        return False

    return valid_episodes, total_show_time


# path = json file
# returns True if multiple speaker tags
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
    

results = collect_files()

with open('valid_shows.txt', 'w') as f:
    for show in results:
        f.write(show)
