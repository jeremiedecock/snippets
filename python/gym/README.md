# OpenAI Gym

    Gym is a toolkit for developing and comparing reinforcement learning
    algorithms. It makes no assumptions about the structure of your agent, and
    is compatible with any numerical computation library, such as TensorFlow or
    Theano.

    The gym library is a collection of test problems — environments — that you
    can use to work out your reinforcement learning algorithms. These
    environments have a shared interface, allowing you to write general
    algorithms.

- Official web site: https://gym.openai.com/
- Getting Started: https://gym.openai.com/docs/

## Install Gym

```pip install gym```

## Optional dependencies

    To install the full set of environments, you'll need to have some system packages installed.
    Also, take a look at the docker files (py.Dockerfile) to see the composition of our CI-tested images.

### Atari games

```pip install gym[atari]```

### MuJoCo

    MuJoCo has a proprietary dependency we can't set up for you.
    Follow the instructions in the mujoco-py package for help.
    As an alternative to mujoco-py, consider PyBullet which uses the open source Bullet physics engine and has no license requirement.

### All dependencies

```pip install 'gym[all]'```

## Troubleshooting

On Debian/Ubuntu, the following error may arise:

    ERROR: Could not find a version that satisfies the requirement opencv-python (from gym) (from versions: none)
    ERROR: No matching distribution found for opencv-python (from gym)

Solution:

```
pip install --upgrade pip
pip install opencv-python
pip install gym
```

https://stackoverflow.com/questions/45293933/could-not-find-a-version-that-satisfies-the-requirement-opencv-python
