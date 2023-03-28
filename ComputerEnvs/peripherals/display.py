from typing import Callable
import attr
import numpy as np
from gymnasium import spaces

from ComputerEnvs.peripherals.base import Peripheral, PeripheralType


class Display(Peripheral):
    name: str = attr.ib(default="display")
    screenshot_fn: Callable[[], np.ndarray] = attr.ib()
    modality_type: PeripheralType = attr.ib(default=PeripheralType.OUTPUT)

    @property
    def observation_space(self):
        return spaces.Box(
            low=0, high=255, shape=self.get_observation().shape, dtype=np.uint8
        )

    def get_observation(self):
        return self.screenshot_fn()
