import json
# same speakerTag
LOCAL_PATH = "data/spotify-podcasts-2020/0" # hardcoded

# path = json file
# returns True if multiple speaker tags
def multiple_speakers(path):
    speaker_tags = {1} # set of speakers
    with open (path) as f:
        data = json.load(f)
    for alt in data['results']:
        for a_dict in alt['alternatives']:
            try:
                trans = a_dict['transcript']
            except:
                trans = None
            try:
                confidence = a_dict['confidence']
            except:
                confidence = None
            try:
                words = a_dict['words']
            except:
                words = None
            for word_dict in words:
                # either all words contain speakerTag or none does
                try:
                    speaker = word_dict['speakerTag']
                    speaker_tags.add(speaker) # constant time compl 
                except:
                    break
    return len(speaker_tags) > 1

res = multiple_speakers(LOCAL_PATH + "/show_60jwFHRBlsK6YsDOup8FWM/6hTdUKMwhZ8hB2pQe8s3ck.json")
print(res)

# non-overlapping (
