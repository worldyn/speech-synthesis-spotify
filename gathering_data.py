import os

LOCAL_DATA_ROOT = './data/spotify-podcasts-2020/podcasts-transcripts/'

REMOTE_AUDIO_ROOT = './Spotify-Podcasts-2020/podcasts-audio-only-2TB/podcasts-audio'

REMOTE_TRANSCRIPT_ROOT = './Spotify-Podcasts-2020/podcasts-no-audio-13GB'


for subdir, dirs, files in os.walk(LOCAL_DATA_ROOT):
    for filename in files:
        podcast_id = filename.split('.')[0]
        remote_audio_path = subdir.replace(LOCAL_DATA_ROOT, REMOTE_AUDIO_ROOT) + '/' + podcast_id + '.ogg'
        remote_audio_path = remote_audio_path.replace('\\','/')
        remote_audio_path = remote_audio_path[1:]

        local_transcript_path = subdir.replace('\\','/')

        os.system('get-data.sh' + ' ' + remote_audio_path + ' ' + local_transcript_path)

        local_ogg_audio_file = local_transcript_path + '/' + podcast_id + '.ogg'
        local_wav_audio_file = local_transcript_path + '/' + podcast_id + '.wav'
        os.system('ffmpeg' + ' ' + '-i'  + ' ' + local_ogg_audio_file + ' ' + local_wav_audio_file)