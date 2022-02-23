import numpy as np
import matplotlib.pyplot as plt

import keyboard
import mouse

from ..base import BaseComputerEnv
from ...peripherals import Keyboard, Mouse
from .display import Display
from .soundtrack import Soundtrack


class LocalGUIEnv(BaseComputerEnv):

    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self,
                 keys=None, buttons=None, monitor_idices=[1],
                 enable_soundtrack=True, microphone=None,
                 samplerate=None, blocksize=None,
                 other_modalities=[]):

        # keyboard
        self.keyboard = Keyboard(
            press_key_fn=keyboard.press,
            release_key_fn=keyboard.release,
            is_pressed_fn=keyboard.is_pressed,
            keys=keys
        )

        # mouse
        self.mouse = Mouse(
            press_button_fn=mouse.press,
            release_button_fn=mouse.release,
            wheel_fn=mouse.wheel,
            move_fn=lambda dx, dy: mouse.move(dx, dy, absolute=False),
            position_fn=mouse.get_position,
            is_pressed_fn=mouse.is_pressed,
            buttons=buttons
        )

        # displays
        self.displays = [Display(monitor_idx=monitor_idx)
                         for monitor_idx in monitor_idices]

        # soundtrack
        if enable_soundtrack:
            self.soundtrack = Soundtrack(
                microphone=microphone,
                samplerate=samplerate,
                blocksize=blocksize
            )

        super().__init__(modalities=[self.keyboard, self.mouse] +
                         ([self.soundtrack] if enable_soundtrack else []) +
                         self.displays + other_modalities)

    def render(self, mode='human'):
        if mode == 'human':
            plt.imshow(self.displays[0].get_observation())
            return plt.show()
        elif mode == 'rgb_array':
            return self.displays[0].get_observation()
        else:
            raise NotImplementedError(f'render mode `{mode}` not supported')
