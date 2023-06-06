import numpy as np
from gymnasium import spaces
import pyte

from ComputaEnv.peripherals.base import Peripheral, PeripheralType


class TerminalDisplay(Peripheral):
    def __init__(self, columns=80, rows=24, name="terminal"):
        super.__init__(modality_type=PeripheralType.OUTPUT, name=name)
        self.columns = columns
        self.rows = rows
        self.screen = pyte.Screen(self.columns, self.lines)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(rows, columns), dtype=np.uint16
        )

    def get_observation(self):
        return self.screen.display
