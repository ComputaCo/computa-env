import numpy as np

import mss

from ComputerEnvs.peripherals import Display as AbstractDisplay


class Monitor(AbstractDisplay):
    def __init__(self, monitor_idx=1, name="display"):
        super().__init__(screenshot_fn=self.get_observation, name=name)
        self.monitor_idx = monitor_idx
        self._sct = mss.mss()
        self._sct.__enter__()

    def __del__(self):
        self._sct.__exit__(None, None, None)

    def get_observation(self):
        im = self._sct.grab(self.monitor_idx)
        frame = np.array(im, dtype=np.uint8)
        # BRGA to RGB
        # https://python-mss.readthedocs.io/examples.html#bgra-to-rgb
        # return np.flip(frame[:, :, :3], 2).tobytes()
        return frame
