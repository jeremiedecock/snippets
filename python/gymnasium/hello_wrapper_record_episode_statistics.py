#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: https://gymnasium.farama.org/introduction/record_agent/

import gymnasium as gym
import numpy as np

NUM_EPISODES = 3

env = gym.make("FrozenLake-v1")
env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=NUM_EPISODES)

observation, info = env.reset()

for episode_index in range(NUM_EPISODES):
    episode_over = False
    while not episode_over:
        action = env.action_space.sample()  # Take a random action
        observation, reward, terminated, truncated, info = env.step(action)
        episode_over = terminated or truncated

env.close()

# Print summary statistics
print(f'\nEvaluation Summary:')
print(f'Episode durations: {list(env.time_queue)}')
print(f'Episode rewards: {list(env.return_queue)}')
print(f'Episode lengths: {list(env.length_queue)}')

# Calculate some useful metrics
avg_reward = np.sum(env.return_queue)
avg_length = np.sum(env.length_queue)
std_reward = np.std(env.return_queue)

print(f'\nAverage reward: {avg_reward:.2f} ± {std_reward:.2f}')
print(f'Average episode length: {avg_length:.1f} steps')
print(f'Success rate: {sum(1 for r in env.return_queue if r > 0) / len(env.return_queue):.1%}')