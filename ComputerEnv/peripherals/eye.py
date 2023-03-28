from typing import Callable, Protocol, runtime_checkable
import attr
import numpy as np
from gymnasium import spaces

from ComputerEnv.peripherals.base import Peripheral, PeripheralType


@runtime_checkable
class ScreenshotFn(Protocol):
    def __call__(
        self, location: tuple[int, int] | np.array, size: tuple[int, int] | np.array
    ) -> np.ndarray:
        ...


@attr.s
class Eye(Peripheral):
    name: str = attr.ib(default="eye")
    screenshot_fn: ScreenshotFn = attr.ib()
    window_size = attr.ib(default=(100, 100))
    location: np.array = attr.ib(default=np.zeros(2))
    modality_type: PeripheralType = attr.ib(default=PeripheralType.OUTPUT)

    @property
    def observation_space(self):
        return spaces.Dict(
            {
                "image": spaces.Box(
                    low=0, high=255, shape=self.window_size, dtype=np.uint8
                ),
                "location": spaces.Box(low=0, high=255, shape=(2,), dtype=np.uint8),
            }
        )

    def get_observation(self):
        return {
            "image": self.screenshot_fn(self.location, self.window_size),
            "location": self.location,
        }

    @property
    def action_space(self):
        return spaces.Box(low=0, high=255, shape=(2,), dtype=np.float32)

    def apply_action(self, action):
        self.location += action
