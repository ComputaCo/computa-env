import numpy as np
from gymnasium import spaces

from .base import Peripheral, PeripheralType


class Mouse(Peripheral):
    """
    Observation space: {
      'position': (float, float),
      'buttons': list[int]
    }
    Action space: {
      'motion': (float, float),
      'wheel_delta': float,
      'buttons': list[int]
    }
    """

    def __init__(
        self,
        press_button_fn,
        release_button_fn,
        wheel_fn,
        move_fn,
        position_fn,
        is_pressed_fn,
        buttons=["left", "right", "middle"],
        name="mouse",
    ):
        super().__init__(modality_type=PeripheralType.BOTH, name=name)
        self.press_button_fn = press_button_fn
        self.release_button_fn = release_button_fn
        self.wheel_fn = wheel_fn
        self.move_fn = move_fn
        self.position_fn = position_fn
        self.is_pressed_fn = is_pressed_fn
        self.buttons = buttons
        self.observation_space = spaces.Dict(
            {
                "position": spaces.Box(low=-np.inf, high=np.inf, shape=(2,)),
                "buttons": spaces.MultiBinary(len(self.buttons)),
            }
        )
        self.action_space = spaces.Dict(
            {
                "motion": spaces.Box(low=-np.inf, high=np.inf, shape=(2,)),
                "wheel": spaces.Box(low=-np.inf, high=np.inf, shape=(1,)),
                "buttons": spaces.MultiBinary(len(self.buttons)),
            }
        )

    def reset(self):
        self.release_button_fn(self.buttons)
        self._button_state = np.zeros(len(self.buttons))

    def get_observation(self):
        return {
            "position": np.array(self.position_fn(), dtype=float),
            "buttons": np.array(
                [self.is_pressed_fn(button) for button in self.buttons], dtype=int
            ),
        }

    def apply_action(self, action):
        self.move_fn(action["motion"])
        self.wheel_fn(action["wheel_delta"])
        button_diff = action["buttons"] - self._button_state
        # press = diff > 0
        # release = diff < 0
        for button, change in zip(self.buttons, button_diff):
            if change > 0:
                self.press_button_fn(button)
            elif change < 0:
                self.release_button_fn(button)
            else:
                pass
