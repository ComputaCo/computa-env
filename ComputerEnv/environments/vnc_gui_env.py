import pyVNC

from .base import BaseComputerEnv
from ..peripherals import Keyboard, Mouse, Display, Soundtrack
from ..peripherals.keyboard.constants import ASCII_128_KEYS


class VNCGUIEnv(BaseComputerEnv):

    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, display_resolution=(640, 480), keyboard):

        self.display
        super.__init__(modalities=[

        ])

    def reset(self):
        return super.reset()

    def render(self, mode='human'):
        if mode == 'human':
            import matplotlib.pyplot as plt
            plt.imshow(self.display.get_observation())
            return plt.show()
        elif mode == 'rgb_array':
            return self.display.get_observation()
        else:
            raise NotImplementedError(f'render mode `{mode}` not supported')
