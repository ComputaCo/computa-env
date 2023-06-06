import numpy as np
import matplotlib.pyplot as plt

from pynput import keyboard as pynput_keyboard
from pynput import mouse as pynput_mouse

from ComputaEnv.environments.base import BaseComputaEnv
from ComputaEnv.peripherals import Keyboard, Mouse
from ComputaEnv.environments.local_gui_env.display import Display
from ComputaEnv.environments.local_gui_env.soundtrack import Soundtrack


class LocalGUIEnv(BaseComputaEnv):
    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(
        self,
        keys=None,
        buttons=None,
        monitor_idices=[1],
        listen_to_soundtrack=True,
        listen_to_mic=False,  # TODO: implement
        output_to_soundtrack=True,  # TODO: implement
        microphone=None,
        samplerate=None,
        blocksize=None,
        other_modalities=[],
    ):
        # keyboard
        self.keyboard_controller = pynput_keyboard.Controller()
        self.keyboard_listener = pynput_keyboard.Listener

        self.keyboard = Keyboard(
            press_key_fn=self.keyboard_controller.press,
            release_key_fn=self.keyboard_controller.release,
            is_pressed_fn=self.is_key_pressed,
            keys=keys,
        )

        # mouse
        self.mouse_controller = pynput_mouse.Controller()
        self.mouse_listener = pynput_mouse.Listener

        self.mouse = Mouse(
            press_button_fn=self.mouse_controller.press,
            release_button_fn=self.mouse_controller.release,
            wheel_fn=self.mouse_controller.scroll,
            move_fn=self.mouse_controller.move,
            position_fn=self.get_mouse_position,
            is_pressed_fn=self.is_button_pressed,
            buttons=buttons,
        )

        # displays
        self.displays = [
            Display(monitor_idx=monitor_idx) for monitor_idx in monitor_idices
        ]

        # soundtrack
        if listen_to_soundtrack:
            self.soundtrack = Soundtrack(
                microphone=microphone, samplerate=samplerate, blocksize=blocksize
            )

        super().__init__(
            modalities=[self.keyboard, self.mouse]
            + ([self.soundtrack] if listen_to_soundtrack else [])
            + self.displays
            + other_modalities
        )

    def is_key_pressed(self, key):
        with self.keyboard_listener(pynput_keyboard.Events()) as listener:
            return listener.is_pressed(key)

    def get_mouse_position(self):
        return self.mouse_controller.position

    def is_button_pressed(self, button):
        with self.mouse_listener(pynput_mouse.Events()) as listener:
            return listener.is_pressed(button)

    def render(self, mode="human"):
        if mode == "human":
            plt.imshow(self.displays[0].get_observation())
            return plt.show()
        elif mode == "rgb_array":
            return self.displays[0].get_observation()
        else:
            raise NotImplementedError(f"render mode `{mode}` not supported")
