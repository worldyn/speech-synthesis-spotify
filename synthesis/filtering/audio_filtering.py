import scipy.io.wavfile
import numpy as np
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic




def pitch_energy(filename):

    signal = basic.SignalObj(filename)
    pitch = pYAAPT.yaapt(signal)

    print(pitch.nframes * pitch.frame_size)

    return pitch.samp_values, pitch.energy
