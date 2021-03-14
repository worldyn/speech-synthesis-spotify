import numpy as np
from scipy.io import wavfile
import parselmouth
from g2p_en import G2p


class Segment:
    def __init__(self, path, start_time, end_time, samp_freq=44100, text=""):
        self.path = path  # episode path
        self.start_time = start_time
        self.end_time = end_time
        self.time = end_time - start_time
        snd = parselmouth.Sound(path)
        self.snd = snd.extract_part(from_time=start_time, to_time=end_time)
        self.data = self.snd.values.T  # amplitudes

        self.samp_freq = samp_freq
        self.intensity = self.snd.to_intensity()
        self.pitch_obj = self.snd.to_pitch()
        self.pitch = self.pitch_obj.selected_array["frequency"]
        self.energy = self.snd.get_energy()

        self.text = text

    def write(self, path):
        wavfile.write(path, self.samp_freq, self.data)

    def pitch_avg(self):
        return np.average(self.pitch)

    def get_energy(self):
        return self.energy

    def intensity_avg(self):
        return np.average(self.intensity)

    def get_speech_rate(self):
        g2p = G2p()
        phonemes = g2p(self.text)
        phonemes = [s for s in phonemes if s.strip()]
        return len(phonemes) / self.time
