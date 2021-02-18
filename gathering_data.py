import os
import time
import logging
import threading
import time
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile


LOCAL_DATA_ROOT = './data/spotify-podcasts-2020/podcasts-transcripts/6/0'

REMOTE_AUDIO_ROOT = './Spotify-Podcasts-2020/podcasts-audio-only-2TB/podcasts-audio/6/0'

REMOTE_TRANSCRIPT_ROOT = './Spotify-Podcasts-2020/podcasts-no-audio-13GB/6/0'

def log_print(filename, text):
    with open(filename, 'a') as file:
        file.write(text)

def collect_files():

    podcasts_ids = []

    for subdir, dirs, files in os.walk(LOCAL_DATA_ROOT):
        for filename in files:

            podcast_id = filename.split('.')[0]

            podcasts_ids.append((subdir, podcast_id))
    
    return podcasts_ids


def retrieve_batch(batch):   

    log_file = 'retrieve.log'

    log_print(log_file, '\n\n### NEW BATCH ###\n')   

    args = ''

    for subdir, podcast_id in batch:

        audio_file = subdir.replace(LOCAL_DATA_ROOT, '') + '/' + podcast_id + '.ogg'
        audio_file = audio_file.replace('\\','/')
        audio_file = audio_file[1:]

        args += ' ' + audio_file

    log_print(log_file, 'Downloading ' + str(len(batch)) + ' audio files...')
    start = time.time()
    os.system('get-data.sh' + args)
    end = time.time()
    log_print(log_file, 'Download of ' + str(len(batch)) + ' files completed in ' + str(end - start))
    log_print(log_file, '\nFiles processed: \n' + str(batch))



def convert_batch(batch):

    log_file = 'convert.log'   

    log_print(log_file, '\n\n### NEW BATCH ###\n')  

    log_print(log_file, 'Converting ' + str(len(batch)) + ' audio files...')
    start = time.time()
    for subdir, podcast_id in batch:

        transcript_path = subdir.replace('\\','/')
        
        ogg_file = transcript_path + '/' + podcast_id + '.ogg'
        wav_file = transcript_path + '/' + podcast_id + '.wav'

        os.system('ffmpeg' + ' ' + '-n'  + ' ' + '-i'  + ' ' + ogg_file + ' ' + wav_file)

    end = time.time()
    log_print(log_file, 'Conversion of ' + str(len(batch)) + ' files completed in ' + str(end - start))
    log_print(log_file, '\nFiles processed: \n' + str(batch))


def make_spectrogram(batch):
    sample_rate, samples = wavfile.read('path-to-mono-audio-file.wav')
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()


def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)


files = collect_files()


workload = len(files)
batch_size = 20

print('Processing ' + str(workload) + ' files with batch size of ' + str(batch_size))

divisions = list(range(0, workload, batch_size))
divisions.append(len(files))

batches = []

for i in range(1,len(divisions)):
    batch = files[divisions[i-1] : divisions[i]]
    batches.append(batch)

# Retrieve the first batch without paralelism
retrieve_batch(batches[0])

# Retrieve the batch[i] while converting the batch[i-1]
for batch_index in range(1,len(batches)):

    convert_thread = threading.Thread(target=convert_batch, args=(batches[batch_index-1],))
    convert_thread.start()

    retrieve_batch(batches[batch_index])

    convert_thread.join()

# Convert the last batch without paralelism
convert_batch(batches[-1])

exit()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")