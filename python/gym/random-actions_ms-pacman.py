#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Src: https://gym.openai.com/docs/#environments

import gym

env = gym.make('MsPacman-v0')
env.reset()

for _ in range(300):
    env.render()
    env.step(env.action_space.sample())      # Take a random action

env.close()
