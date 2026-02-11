#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: https://gymnasium.farama.org/api/vector/

import gymnasium as gym
import numpy as np

# Create a vectorized environment with 4 parallel sub-environments.
# In "async" mode each sub-environment runs in its own process,
# so steps execute truly in parallel (useful for heavy envs).
num_envs = 4
envs = gym.make_vec("FrozenLake-v1", num_envs=num_envs, vectorization_mode="async")

print(f"Number of parallel environments: {envs.num_envs}")
print(f"Observation space: {envs.observation_space}")
print(f"Action space: {envs.action_space}\n")

observations, infos = envs.reset(seed=42)

# In a VectorEnv, sub-environments that terminate are automatically
# reset — they never stop running. We therefore run for a fixed
# number of steps and track episode completions ourselves.
total_steps = 50
episode_counts = np.zeros(num_envs, dtype=int)
episode_returns = np.zeros(num_envs)

for step in range(1, total_steps + 1):
    actions = envs.action_space.sample()
    observations, rewards, terminateds, truncateds, infos = envs.step(actions)

    episode_returns += rewards
    dones = terminateds | truncateds

    print(f"  Observations: {observations}")
    print(f"  Rewards: {rewards}")
    print(f"  Terminateds: {terminateds}")
    print(f"  Truncateds: {truncateds}")

    # Show which environments completed
    for i, done in enumerate(dones):
        if done:
            print(f"  Environment {i} completed!")
    
    print()

print(f"\nTotal episodes completed per env: {episode_counts}")
print(f"Grand total episodes: {episode_counts.sum()}")

envs.close()