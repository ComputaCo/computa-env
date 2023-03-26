import numpy as np
from gymnasium import spaces

from ..base import Peripheral, PeripheralType
from .constants import STANDARD_ENGLISH_US_KEYBOARD_KEYS


class Keyboard(Peripheral):
    """
    If `is_pressed_fn` is None, it will be taken from the internal key_state.
    """

    def __init__(
        self,
        press_key_fn,
        release_key_fn,
        is_pressed_fn=None,
        keys=None,
        name="keyboard",
    ):
        super().__init__(modality_type=PeripheralType.BOTH, name=name)
        self.press_key_fn = press_key_fn
        self.release_key_fn = release_key_fn
        self.is_pressed_fn = is_pressed_fn
        self.keys = keys or STANDARD_ENGLISH_US_KEYBOARD_KEYS
        self.observation_space = spaces.MultiBinary(len(self.keys))
        self.action_space = spaces.MultiBinary(len(self.keys))
        self.reset()

    def reset(self):
        self.release_key_fn(self.keys)
        self._key_state = np.zeros(len(self.keys))

    def get_observation(self):
        if self.is_pressed_fn:
            # this is repetitive and unnecesary if no other processes or users
            # are interacting with the computer's keyboard while the agent is running
            # but it is useful for multi-agent collaboration. It also allows for
            # sensorimotor feedback.
            self._key_state = np.array(
                [self.is_pressed_fn(key) for key in self.keys], dtype=int
            )
        return self._key_state

    def apply_action(self, action):
        diff = action - self._key_state
        # press = diff > 0
        # release = diff < 0
        for key, change in zip(self.keys, diff):
            if change > 0:
                self.press_key_fn(key)
            elif change < 0:
                self.release_key_fn(key)
            else:
                pass
