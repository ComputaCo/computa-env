import numpy as np
from gymnasium import spaces

from .base import Peripheral, PeripheralType


class Display(Peripheral):
    def __init__(self, screenshot_fn, name="display"):
        super.__init__(modality_type=PeripheralType.OUTPUT, name=name)
        self.screenshot_fn = screenshot_fn

    @property
    def observation_space(self):
        return spaces.Box(
            low=0, high=255, shape=self.get_observation().shape, dtype=np.uint8
        )

    def get_observation(self):
        return self.screenshot_fn()
