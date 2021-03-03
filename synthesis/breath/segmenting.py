import numpy as np

def load_dummy():
    # return np.array([0,1,1,1,1])
    return np.load("./arr_0.npy")

def trans_in_seconds(arr):
    arr = np.array(arr) * 0.05
    return arr

if __name__ == "__main__":
    arr = load_dummy()
    start = -2
    end = -1
    result_arr = []

    for index,a in enumerate(arr):
        if a == 1:
            if arr[index-1] != 1 or index == 0:
                start = index
            if index == len(arr)-1 or arr[index+1] != 1:
                end = index
                result_arr.append([start,end])
    print(result_arr)
    print(trans_in_seconds(result_arr))

