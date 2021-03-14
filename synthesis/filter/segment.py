from functools import lru_cache
from cached_property import cached_property
import numpy as np
from scipy.io import wavfile
import parselmouth
from g2p_en import G2p


class Segment:
    def __init__(self, path, start_time, end_time, samp_freq=44100, text=""):
        self.path = path
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time

        sound = read_sound_file(path).extract_part(
            from_time=start_time, to_time=end_time
        )
        self.amplitudes = sound.values.T

        self.samp_freq = samp_freq
        self.intensities = sound.to_intensity()
        self.pitches = sound.to_pitch().selected_array["frequency"]
        self.energy = sound.get_energy()

        self.text = text

    def write(self, path):
        wavfile.write(path, self.samp_freq, self.amplitudes)

    @cached_property
    def pitch(self):
        return np.mean(self.pitches)

    @cached_property
    def intensity(self):
        return np.mean(self.intensities)

    @cached_property
    def speech_rate(self):
        g2p = G2p()
        phonemes = g2p(self.text)
        phonemes = [s for s in phonemes if s.strip()]
        return len(phonemes) / self.duration

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.path, self.start_time, self.end_time, self.text))


@lru_cache(maxsize=1)
def read_sound_file(path):
    return parselmouth.Sound(path)
