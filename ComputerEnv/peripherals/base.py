import enum


class PeripheralType(enum.Enum):
    INPUT = 0  # input to computer. eg. keyboard
    OUTPUT = 1  # output from computer. eg. terminal
    BOTH = 2  # both input and output


class Peripheral:

    def __init__(self, modality_type, name):
        self.modality_type = modality_type
        self.name = name

    def reset(self):
        """Optional method to reset the peripheral to its initial state.
        Useful when entering a new computing environment or 
        restarting control over an existing one"""
        pass

    def get_observation(self):
        raise NotImplementedError(
            'This method must be implemented by a subclass.')

    def apply_action(self, action):
        raise NotImplementedError(
            'This method must be implemented by a subclass.')

    @property
    def observation_space(self):
        return None

    @property
    def action_space(self):
        return None
