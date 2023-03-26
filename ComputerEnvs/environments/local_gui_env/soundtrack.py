import numpy as np
import soundcard as sc
from ...peripherals import Soundtrack as AbstractSoundtrack


class Soundtrack(AbstractSoundtrack):
    def __init__(
        self, microphone=None, samplerate=16000, blocksize=64, name="soundtrack"
    ):
        mic = microphone or sc.default_microphone()
        self.recorder = mic.recorder(samplerate=samplerate, blocksize=blocksize)
        self.recorder.__enter__()
        super().__init__(record_frames_fn=lambda: self.recorder.record(), name=name)

    def __del__(self):
        self.recorder.__exit__()
        super().__del__()
