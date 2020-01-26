#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Src: https://gym.openai.com/docs/#environments

import gym

env = gym.make('CartPole-v0')

for i_episode in range(3):
    observation = env.reset()

    for t in range(100):
        env.render()
        print(observation)

        action = env.action_space.sample()      # Take a random action
        observation, reward, done, info = env.step(action)

        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

env.close()