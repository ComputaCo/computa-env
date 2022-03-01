# computer_env

:construction: **This repository is under construction.** :construction: Stable release coming this Summer 2022.

Want to contribute? Check out the GitHub container repository [Limboid/the-artificial-ecosystem](https://github.com/Limboid/the-artificial-ecosystem) for this project.

`computer_env` is a gym-style environment for developing machine learning agents that interact with a computer.

## The Problem

**The holy grail of machine learning**:

> Can we make a machine learning agent obey high-level natural language instructions to automate computer work?

Examples:
- `Look for bugs in the tensorflow library and fix them`
- `Write a program that efficiently transpiles javascript to C++`
- `Start a dropshipping LLC in Deloware. Prepare all the contracts that are needed and ask me to sign them.`

I think `computer_env` is an important step in this direction.

## Getting Started

First, you'll need to install `computer_env`:

```bash
pip install computer-env  # not available yet
```

Then, you can create a new environment:

```python
from computer_env import LocalGUIEnv
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

ComputerEnv modalities are passed in at initialization time. Subclasses like `LocalComputerEnv` and `VNCComputerEnv` provide convenience initialization for several standard modalities. However, you can easily introduce you own modalities by subclassing the `ComputerModality` class:

```python
# TODO make this example work

from computer_env import ComputerEnv, ComputerModality, LocalComputerEnv

class TouchModality(ComputerModality):
    def __init__(self, num_fingers = 2, screen_size: Tuple[int, int]):
      ...
      super().__init__(
          name='touch',
          action_space=gym.spaces.Discrete(2), # or None if not applicable
          observation_space=gym.spaces.Box(low=0, high=1, shape=(2,), dtype=np.uint8), # or None if not applicable
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

env = ComputerEnv(modalities=LocalComputerEnv.modalities + [MyModality()])
```

## Standard Modalities

```python
from computer_env import LocalComputerEnv
print(LocalComputerEnv.observation_modalities)
# TODO
print(LocalComputerEnv.action_modalities)
# TODO
```

# TODO list all standard modalities

```python
from computer_env import VNCComputerEnv
print(VNCComputerEnv.observation_modalities)
# TODO
print(VNCComputerEnv.action_modalities)
# TODO
```

## TODO: STANDARD OPEN SOURCE REPO TEMPLATE README SECTIONS
