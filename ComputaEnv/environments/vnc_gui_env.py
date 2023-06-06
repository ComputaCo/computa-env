import subprocess
from typing import Optional
import pyVNC

from ComputaEnv.environments.base import BaseComputaEnv
from ComputaEnv.peripherals import Keyboard, Mouse, Display
from ComputaEnv.peripherals.keyboard.constants import ASCII_128_KEYS


class VNCGUIEnv(BaseComputaEnv):
    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(
        self,
        keys=ASCII_128_KEYS,
        buttons=None,
        display_resolution=(640, 480),
        create_new=True,
        vnc_host=None,
        vnc_port=None,
        vnc_password=None,
    ):
        if vnc_host is None:
            vnc_port = vnc_port or 5900
            vnc_password = vnc_password or "password"
            create_new = False
        if create_new:
            vnc_host, vnc_port, vnc_password = self.create_new_vnc_server(
                display_resolution
            )

        self.vnc_client = pyVNC.Client(
            host=vnc_host, port=vnc_port, password=vnc_password, gui=True
        )
        self.vnc_client.start()

        self.display = Display(
            get_frame_fn=self.vnc_client.screen.get_array, resolution=display_resolution
        )

        self.keyboard = Keyboard(
            press_key_fn=self.vnc_client.send_press,
            release_key_fn=self.vnc_client.send_release,
            is_pressed_fn=None,
            keys=ASCII_128_KEYS,
        )

        self.mouse = Mouse(
            press_button_fn=lambda button: self.vnc_client.send_mouse(
                event=button, position=self.mouse.position_fn()
            ),
            release_button_fn=lambda button: self.vnc_client.send_mouse(
                event=button, position=self.mouse.position_fn()
            ),
            wheel_fn=None,
            move_fn=lambda x, y: self.vnc_client.send_mouse(position=(x, y)),
            position_fn=None,
            is_pressed_fn=None,
            buttons=pyVNC.constants.MOUSE_BUTTONS,
        )

        super().__init__(modalities=[self.keyboard, self.mouse, self.display])

    def reset(self):
        return super().reset()

    def render(self, mode="human"):
        if mode == "human":
            import matplotlib.pyplot as plt

            plt.imshow(self.display.get_observation())
            return plt.show()
        elif mode == "rgb_array":
            return self.display.get_observation()
        else:
            raise NotImplementedError(f"render mode `{mode}` not supported")

    def close(self):
        self.vnc_client.join()

    _vnc_server_proc: Optional[subprocess.Popen] = None
    _DISPLAY_NUM = 1  # class variable, not instance variable

    def create_new_vnc_server(
        display_resolution: tuple[int, int]
    ) -> tuple[str, int, Optional[str]]:
        global _vnc_server_proc

        if _vnc_server_proc:
            raise RuntimeError(
                "A VNC server process is already running. Close the existing process before creating a new one."
            )

        # Customize the following variables based on your specific VNC setup
        display_num, VNCGUIEnv._DISPLAY_NUM = (
            VNCGUIEnv._DISPLAY_NUM,
            VNCGUIEnv._DISPLAY_NUM + 1,
        )  # Adjusts the display number to avoid conflicts with other VNC servers
        vnc_password = None  # Set a password or leave it as None for no password

        resolution_arg = f"{display_resolution[0]}x{display_resolution[1]}"
        display_arg = f":{display_num}"

        command = [
            "Xvnc",  # The VNC server executable, which may vary depending on the VNC server software you are using
            display_arg,
            "-geometry",
            resolution_arg,
            "-SecurityTypes",
            "None" if vnc_password is None else "VncAuth",
            "-PasswordFile",
            "/path/to/password/file" if vnc_password else "",
        ]

        self._vnc_server_proc = subprocess.Popen(command)

        vnc_host = "localhost"
        vnc_port = 5900 + display_num

        return vnc_host, vnc_port, vnc_password

    def close_vnc_server():
        global self._vnc_server_proc
        if _vnc_server_proc:
            _vnc_server_proc.terminate()
            _vnc_server_proc.wait()
            _vnc_server_proc = None
