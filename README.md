:warning: ComputaEnv is not working yet. It is still in the design phase. Please see https://github.com/ComputaCo/computer-env/issues/1 :warning:

# computa_env

`computa_env` is a gym-style environment for developing machine learning agents that interact with a computer.

## Getting Started

First, you'll need to install `computa_env`:

```bash
pip install computer-env  # not available yet
```

Then, you can create a new environment:

```python
from computa_env import LocalGUIEnv
env = LocalGUIEnv()
# We also offer VNCGUIEnv, ChromeEnv, StdioEnv, and AndroidEnv
```

Call `reset()` to start a new episode:

```python
observation = env.reset()
```

Now you can interact with the environment just like any other gym environment:

```python
while True:
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print(observation, reward, done, info)
```

## Features

- General purpose gym-compatible computer interaction environment
- Supports multiple agents sharing the same machine simultaneously (including you!)

- `LocalGUIEnv` provides system keyboard i/o, mouse i/o, and audiovideo output
- `VNCGUIEnv` provides a connection to a VNC server with mouse i/o, keyboard i/o, and video output
- `ChromeEnv` provides a connection to a Chrome browser with mouse i/o, keyboard i/o, and video output
- `StdioEnv` provides a connection to a system process with keyboard i/o and ansi terminal output
- `AndroidEnv` provides a connection to an Android device with touch i/o, keyboard input, and audiovideo output

## Concepts

The action sent in the `step(action)` method is merely a request for the computer to execute that action. Other processes may be controlling the keyboard, mouse, audio, and other devices. This means you, other agents, or bots may be able to simultaneously operate on the same computer, but it also means the agent could be 'surprised' by the computer's behavior. For example, the `release_key` action might not always result in a `key_pressed` observation if another user is still holding the key down.

ComputaEnv modalities are passed in at initialization time. Subclasses like `LocalComputaEnv` and `VNCComputaEnv` provide convenience initialization for several standard modalities. However, you can easily introduce you own modalities by subclassing the `ComputerModality` class:

```python
# TODO make this example work

from computa_env import ComputaEnv, ComputerModality, LocalComputaEnv

class TouchModality(ComputerModality):
    def __init__(self, num_fingers = 2, screen_size: Tuple[int, int]):
      ...
      super().__init__(
          name='touch',
<<<<<<< HEAD
          action_space=spaces.Discrete(2), # or None if not applicable
          observation_space=spaces.Box(low=0, high=1, shape=(2,), dtype=np.uint8), # or None if not applicable
=======
          action_space=gym.spaces.Discrete(2), # or None if not applicable
          observation_space=gym.spaces.Box(low=0, high=1, shape=(2,), dtype=np.uint8), # or None if not applicable
>>>>>>> d9f4883863ce60672e075a784f94e72269e05950
          device='mouse',
          device_args={'button': 1},
      )
      ...

    def observe(self):
      # not needed if TouchModality were an action-only modality
      ...
      
    def act(self, action):
      # not needed if TouchModality were an observation-only modality
      ...

env = ComputaEnv(modalities=LocalComputaEnv.modalities + [MyModality()])
```

## Standard Modalities

```python
from computa_env import LocalComputaEnv
print(LocalComputaEnv.observation_modalities)
# TODO
print(LocalComputaEnv.action_modalities)
# TODO
```

# TODO list all standard modalities

```python
from computa_env import VNCComputaEnv
print(VNCComputaEnv.observation_modalities)
# TODO
print(VNCComputaEnv.action_modalities)
# TODO
```

## TODO: STANDARD OPEN SOURCE REPO TEMPLATE README SECTIONS
<<<<<<< HEAD


## Major TODO's

- `num_fingers` shouldn't be a parameter. It should be a separate modality `Finger(screen)`. Likewise, using xinput for multiple cursors, you should be able to do `Mouse(screen)`, and a `supports_multimouse` environment will be able to respond intelligently. More generally, there should be a corresponding Environment protocol for all modalities: `supports_keyboard`, `supports_touch`, etc., and maybe there should be a `supports_X = make_protocol(modality_X)` meta-function.
=======
>>>>>>> d9f4883863ce60672e075a784f94e72269e05950
