import os
import pty
import pyte
import subprocess

from .base import BaseComputerEnv
from ..peripherals import Keyboard, TerminalDisplay
from ..peripherals.keyboard.constants import ASCII_128_KEYS


class StdIOEnv(BaseComputerEnv):

    metadata = {"render.modes": ["human", "ansi"]}

    def __init__(
        self,
        keys=ASCII_128_KEYS,
        columns=80,
        rows=24,
        buffer_size=4096,
        command="bash",
        cwd=None,
        env=None,
    ):

        # keyboard
        self.keyboard = Keyboard(
            press_key_fn=lambda key: None, release_key_fn=lambda key: None, keys=keys
        )

        # terminal display
        self.terminal_display = TerminalDisplay(columns=columns, rows=rows)
        self.stream = pyte.ByteStream(self.terminal_display.screen)

        # process args
        self.buffer_size = buffer_size
        self.command = command
        self.cwd = cwd or os.getcwd()
        self.env = env or dict()
        # recommended from `nle` and `pyte` code / examples
        self.env.update(
            dict(
                TERM="linux",
                COLUMNS=self.terminal_display.columns,
                LINES=self.terminal_display.rows,
            )
        )

        self.subprocess = None

        super.__init__(modalities=[self.keyboard, self.terminal_display])

    def __del__(self):
        self._close_subprocess()

    def reset(self):
        # reset screen
        self.terminal_display.screen.reset()

        # start subprocess
        if self.subprocess:
            self._close_subprocess()
        self.subprocess = subprocess.Popen(
            self.command,
            bufsize=self.buffer_size,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=self.cwd,
            env=self.env,
        )
        return super().reset()

    def step(self, action):
        # skip super.step() and self._apply_action(action)
        # since there is only one modality, the action is directly applied

        # type to stdin
        keys_down = [
            key
            for idx, key in enumerate(self.keyboard.keys)
            if self.keyboard._key_state[idx]
        ]
        # StdioKeyboard keys are already in bytes
        self.subprocess.stdin.write(bytes(keys_down))

        # the running program manages what should be piped to stdout (which is the terminal display)
        # self.stream.feed(stdin)

        # read stdout to terminal display
        self.stream.feed(self.subprocess.stdout.read().decode("utf-8"))

        # use superclass method because both the keyboard and
        # terminal display are output modalities
        return self._get_observation()

    def render(self, mode="human"):
        if mode == "human":
            import matplotlib.pyplot as plt

            # TODO: plot screen to matplotlib
            return plt.show()
        elif mode == "ansi":
            return self.terminal_display.screen
        else:
            raise NotImplementedError(f"render mode `{mode}` not supported")

    def _close_subprocess(self):
        self.subprocess.kill()
        del self.subprocess
        self.subprocess = None
