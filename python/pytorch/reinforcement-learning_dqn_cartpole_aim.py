#!/usr/bin/env python3
# coding: utf-8

"""
Reinforcement Learning with Vanilla DQN (Deep Q-Network)

Notes: this naive implementation does't use buffer replay and target network.
       Thus, it has very little chance to actually solve the CartPole-v1 problem!
       This is just a base used to build more advanced implementations.
"""

import aim
import gymnasium as gym
import itertools
import random
import torch


# PARAMETERS ###################################################################

GYM_ENVIRONMENT_NAME = "CartPole-v1"
PTH_FILE_NAME = "dqn_cartpole.pth"

DO_TRAINING = True
DO_INFERENCE = True

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# TRAINING PARAMETERS

NN_L1 = 32            # The number of neurons in the first layer
NN_L2 = 32            # The number of neurons in the second layer

GAMMA = 0.99          # The discount factor
EPSILON = 0.05        # the starting value of epsilon
LR = 1e-4             # The learning rate of the ``AdamW`` optimizer

NUM_EPISODES = 500   # The number of episodes to train for


# ACTION-VALUE FUNCTION ESTIMATION ############################################

class QNetwork(torch.nn.Module):

    def __init__(self, n_observations, n_actions):
        super(QNetwork, self).__init__()
        self.layer1 = torch.nn.Linear(n_observations, NN_L1)
        self.layer2 = torch.nn.Linear(NN_L1, NN_L2)
        self.layer3 = torch.nn.Linear(NN_L2, n_actions)

    def forward(self, x):
        x = torch.nn.functional.relu(self.layer1(x))
        x = torch.nn.functional.relu(self.layer2(x))
        return self.layer3(x)


# EPSILON-GREEDY ##############################################################

class EpsilonGreedy:
    def __init__(self, epsilon: float, env: gym.Env, policy_network):
        self.epsilon = epsilon
        self.env = env
        self.policy_network = policy_network
    
    def __call__(self, state):
        """Select action with epsilon-greedy policy"""

        if random.random() < self.epsilon:
            action = self.env.action_space.sample()
        else:
            with torch.no_grad():
                state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)

                q_values = self.policy_network(state_tensor)
                action = q_values.argmax().item()
        
        return action


# TRAINING ####################################################################

def train():
    # INITIALIZE AIM

    aim_run = aim.Run()

    # LOG PARAMETERS WITH AIM

    aim_run["hparams"] = {
        "environment_name": GYM_ENVIRONMENT_NAME,
        "nn_l1": NN_L1,
        "nn_l2": NN_L2,
        "gamma": GAMMA,
        "learning_rate": LR,
        "epsilon": EPSILON,
        "learning_rate": LR,
        "num_episodes": NUM_EPISODES,
    }

    print("\n\n" + "*"*80)
    print("Type this in another therminal: aim up")
    print("and open in your web browser the printed URL (e.g. http://127.0.0.1:43800/)")
    print("*"*80, "\n\n")

    # SET UP THE ENVIRONMENT

    env = gym.make(GYM_ENVIRONMENT_NAME)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    # INSTANTIATE REQUIRED OBJECTS

    q_network = QNetwork(state_dim, action_dim).to(device)
    optimizer = torch.optim.AdamW(q_network.parameters(), lr=LR, amsgrad=True)
    loss_fn = torch.nn.MSELoss()

    epsilon_greedy = EpsilonGreedy(EPSILON, env, q_network)

    # TRAINING LOOP

    for episode_index in range(NUM_EPISODES):
        state, info = env.reset()
        episode_reward = 0

        for t in itertools.count():
            action = epsilon_greedy(state)

            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            episode_reward += reward

            # Update the q_network weights
            with torch.no_grad():
                next_state_tensor = torch.tensor(next_state, dtype=torch.float32, device=device).unsqueeze(0)
                target = reward + GAMMA * q_network(next_state_tensor).max()

            state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
            q_values = q_network(state_tensor)
            q_value_of_action = q_values[0, action]

            loss = loss_fn(q_value_of_action, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Log the episode reward
            if done:
                print(f"Episode {episode_index+1}/{NUM_EPISODES}: duration={episode_reward}")
                aim_run.track(episode_reward, name='episode_reward', step=episode_index, context={ "subset": "train" })
                break

            # Update the state
            state = next_state


    # SAVE THE ACTION-VALUE ESTIMATION FUNCTION ###################################

    torch.save(q_network, PTH_FILE_NAME)

    del q_network   # Remove to demonstrate saving and loading
    env.close()

###############################################################################
###############################################################################
###############################################################################

def inference():

    # INSTANTIATE REQUIRED OBJECTS

    env = gym.make(GYM_ENVIRONMENT_NAME, render_mode="human")
    q_network = torch.load(PTH_FILE_NAME).to(device)
    epsilon_greedy = EpsilonGreedy(EPSILON, env, q_network)

    # EPISODES LOOP

    while True:
        state, info = env.reset()
        done = False

        while not done:
            action = epsilon_greedy(state)

            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            state = next_state

    #env.close()


###############################################################################

def main():
    if DO_TRAINING:
        train()

    if DO_INFERENCE:
        inference()

if __name__ == '__main__':
    main()