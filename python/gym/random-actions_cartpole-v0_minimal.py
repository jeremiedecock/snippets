#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Src: https://gym.openai.com/docs/#environments

import gym

env = gym.make('CartPole-v0')

observation = env.reset()
done = False

while not done:
    action = env.action_space.sample()                  # Take a random action
    observation, reward, done, info = env.step(action)
    #print(".", end="")

env.close()