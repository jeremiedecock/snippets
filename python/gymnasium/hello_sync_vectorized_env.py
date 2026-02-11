#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: https://gymnasium.farama.org/api/vector/

import gymnasium as gym
import numpy as np

# Create a vectorized environment with 4 parallel environments
num_envs = 4
envs = gym.make_vec("FrozenLake-v1", num_envs=num_envs, vectorization_mode="sync")

print(f"Number of parallel environments: {envs.num_envs}\n")
print(f"Observation space: {envs.observation_space}")
print(f"Action space: {envs.action_space}")

observations, infos = envs.reset()
print(f"Initial observations: {observations}")
print()

# Track which environments are still running
active_envs = np.ones(num_envs, dtype=bool)
step_count = 0
max_steps = 100  # Limit total steps for demonstration

while active_envs.any() and step_count < max_steps:
    # Sample random actions for all environments
    actions = envs.action_space.sample()
    print(f"Step {step_count + 1} - Actions: {actions}")

    # Step all environments simultaneously
    observations, rewards, terminateds, truncateds, infos = envs.step(actions)

    # Check which environments finished this step
    dones = terminateds | truncateds

    print(f"  Observations: {observations}")
    print(f"  Rewards: {rewards}")
    print(f"  Terminateds: {terminateds}")
    print(f"  Truncateds: {truncateds}")

    # Show which environments completed
    for i, done in enumerate(dones):
        if done and active_envs[i]:
            print(f"  Environment {i} completed!")
            active_envs[i] = False

    print()
    step_count += 1

print(f"Simulation ended after {step_count} steps")
print(f"Active environments remaining: {active_envs.sum()}")

envs.close()