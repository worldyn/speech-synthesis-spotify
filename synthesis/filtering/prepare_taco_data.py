import numpy as np
import json

# Constants
INPUT_FILENAME = 'filtered/filtered_show.json'
TRAIN_OUTPUT = 'ljs_audio_text_train_filelist.txt'
VAL_OUTPUT = 'ljs_dataset_folder/ljs_audio_text_val_filelist.txt'
TEST_OUTPUT = 'ljs_dataset_folder/ljs_audio_text_test_filelist.txt'
TRAIN_PERCENT = 0.95
VAL_PERCENT = 0.04
TEST_PERCENT = 0.01 

def main():
    # Loading the intervals from INTERVAL_FILE
    assert TRAIN_PERCENT + VAL_PERCENT + TEST_PERCENT == 1.0
    print("=> Loading data...")
    with open(INPUT_FILENAME) as file:
         segments = json.load(file)

    #print(segments)

    # Loading the data
    paths = segments["paths"]
    #timestamps = segments["timestamps"]
    transcripts = segments["transcripts"]

    assert len(paths) == len(transcripts)
    print("=> Data Loaded...")

    n_data = len(paths)
    n_train = int(TRAIN_PERCENT * n_data)
    n_val = int(VAL_PERCENT * n_data)
    n_test = int(TEST_PERCENT * n_data)
    print("=> Number of data points in total: ", n_data)
    print("=> n_train {}, n_val {}, n_test {}"\
        .format(n_train,n_val,n_test))

    # remove from test if too big
    if n_train+n_val+n_test > n_data:
        n_test -= n_train+n_val+n_test - n_data

    assert n_train+n_val+n_test <= n_data

    train_idx = n_train 
    val_idx = train_idx + n_val
    test_idx = val_idx + n_test

    print("=> Writing Tacotron Train data file...")
    with open(TRAIN_OUTPUT,'w') as f:
        for i in range(0, train_idx):
            path = paths[i]
            text = transcripts[i]
            f.write(path + "|" + text + "\n")
    
    print("=> Writing Tacotron Validation data file...")
    with open(VAL_OUTPUT,'w') as f:
        for i in range(train_idx, val_idx):
            path = paths[i]
            text = transcripts[i]
            f.write(path + "|" + text + "\n")

    print("=> Writing the rest to Tacotron test data file...")
    with open(TEST_OUTPUT,'w') as f:
        for i in range(val_idx, test_idx):
            path = paths[i]
            text = transcripts[i]
            f.write(path + "|" + text + "\n")

    print("=> Write complete...")


if __name__ == '__main__':
    main()
 



