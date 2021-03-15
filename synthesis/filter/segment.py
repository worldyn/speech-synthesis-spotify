import re
from functools import lru_cache
from cached_property import cached_property
import numpy as np
from scipy.io import wavfile
import parselmouth


class Segment:
    def __init__(self, path, start_time, end_time, text, sample_rate=44100):
        self.path = path
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time

        sound: parselmouth.Sound = read_sound_file(path).extract_part(
            from_time=start_time, to_time=end_time
        )
        self.amplitudes = sound.values.T

        self.sample_rate = sample_rate
        self.intensity = np.mean(sound.to_intensity(subtract_mean=False))
        self.pitch = np.mean(sound.to_pitch().selected_array["frequency"])
        self.energy = sound.get_energy()

        self.text = text

    def write(self, path):
        wavfile.write(path, self.sample_rate, self.amplitudes)

    @cached_property
    def speech_rate(self):
        vowel_groups = re.findall("[aeiou]+", self.text)
        return len(vowel_groups) / self.duration

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.path, self.start_time, self.end_time, self.text))


@lru_cache(maxsize=1)
def read_sound_file(path) -> parselmouth.Sound:
    return parselmouth.Sound(path)
