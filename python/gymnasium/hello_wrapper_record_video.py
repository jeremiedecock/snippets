#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: https://gymnasium.farama.org/introduction/record_agent/

import gymnasium as gym

env = gym.make("FrozenLake-v1", render_mode="rgb_array")
env = gym.wrappers.RecordVideo(
    env,
    video_folder=".",
    name_prefix="hello_wrapper_record_video",
    episode_trigger=lambda x: True    # Record every episode
)

observation, info = env.reset()

episode_over = False
while not episode_over:
    action = env.action_space.sample()  # Take a random action
    observation, reward, terminated, truncated, info = env.step(action)
    episode_over = terminated or truncated

env.close()