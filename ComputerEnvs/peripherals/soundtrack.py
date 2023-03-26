from threading import Thread
from queue import Queue
import numpy as np
from gymnasium import spaces
from ComputerEnvs.peripherals.base import Peripheral, PeripheralType


class Soundtrack(Peripheral):
    """
    Assumes 16-bit samples with 8kHz default sampling rate.
    record_frames_fn: (samplerate, numframes) -> np.ndarray [shape=(frames, channels), dtype=np.int16]
    """

    def __init__(self, record_frames_fn, name="soundtrack"):
        super().__init__(modality_type=PeripheralType.OUTPUT, name=name)
        self.record_frames_fn = record_frames_fn
        self.rec_thread = None
        self.queue = Queue()
        self.observation_space = spaces.Box(
            low=0, high=int(2**16 - 1), shape=(None,), dtype=np.uint16
        )

    def __del__(self):
        if self.rec_thread:
            self.rec_thread.join()

    def reset(self):
        if self.rec_thread:
            self.rec_thread.join()
        self.queue.clear()
        self.rec_thread = Thread(target=self._record_loop, args=(self,))
        self.rec_thread.start()

    def _record_loop(self):
        while True:
            self.queue.put(self.record_frames_fn())

    def get_observation(self):
        # combine all chunks on queue
        chunks = []
        while not self.queue.empty():
            chunks.append(self.queue.get())
        return np.concatenate(chunks) if chunks else np.array([])
