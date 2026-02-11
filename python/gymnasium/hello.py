#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: https://gymnasium.farama.org/introduction/basic_usage/

import gymnasium as gym

env = gym.make("FrozenLake-v1")

observation, info = env.reset()
print(f"Initial observation: {observation}, Info: {info}")

episode_over = False
while not episode_over:
    action = env.action_space.sample()  # Take a random action
    print(f"Action taken: {action}")

    observation, reward, terminated, truncated, info = env.step(action)

    episode_over = terminated or truncated

    print(f"Observation: {observation}, Reward: {reward}, Terminated: {terminated}, Truncated: {truncated}")

env.close()