from typing import Dict, List, Tuple
import numpy as np
import gym
import gym.spaces

from ..peripherals.base import PeripheralType


class BaseComputerEnv:

    metadata = {'render.modes': ['human']}

    def __init__(self, modalities):
        self.modalities = modalities

    @property
    def observation_space(self):
        return gym.spaces.Dict({
            modality.name: modality.observation_space
            for modality in self.modalities
            if modality.peripheral_type in [PeripheralType.OUTPUT, PeripheralType.BOTH]})

    @property
    def action_space(self):
        return gym.spaces.Dict({
            modality.name: modality.action_space
            for modality in self.modalities
            if modality.peripheral_type in [PeripheralType.INPUT, PeripheralType.BOTH]})

    def reset(self):
        for modality in self.modalities:
            modality.reset()
        return self._get_observation()

    def step(self, action):
        self._apply_action(action)
        obs = self._get_observation()
        return obs, 0.0, False, {}  # obs, reward, done, info

    def render(self, mode='human'):
        raise NotImplementedError(
            'This method must be implemented by a subclass.')

    def _get_observation(self):
        return {modality.name: modality.get_observation()
                for modality in self.modalities
                if modality.peripheral_type in [PeripheralType.OUTPUT, PeripheralType.BOTH]}

    def _apply_action(self, action):
        for modality in self.modalities:
            # this gracefully ignores missed keys
            if modality.name in action and modality.peripheral_type in [PeripheralType.INPUT, PeripheralType.BOTH]:
                modality.apply_action(action[modality.name])
