#!/usr/bin/env python3
# coding: utf-8

"""
Reinforcement Learning with DQN (Deep Q-Network)
"""

import aim
import aim.pytorch
import collections
import gymnasium as gym
import itertools
import numpy as np
import random
import torch
from typing import Tuple


# PARAMETERS ###################################################################

GYM_ENVIRONMENT_NAME = "CartPole-v1"
PTH_FILE_NAME = "dqn_cartpole.pth"

DO_TRAINING = True
DO_INFERENCE = True

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# AIM PARAMETERS

AIM_EXPERIMENT_NAME = "reinforcement-learning_dqn-buffer-replay_cartpole"
AIM_TRACK_WEIGHTS = True
AIM_TRACK_GRADIENTS = True

# TRAINING PARAMETERS

NN_L1 = 128            # The number of neurons in the first layer
NN_L2 = 128            # The number of neurons in the second layer

GAMMA = 0.99          # The discount factor
EPSILON_START = 1.0   # The starting value of epsilon
EPSILON_MIN = 0.001   # The minimum value of epsilon
EPSILON_DECAY = 0.999 # The decay rate of epsilon
LR = 1e-4             # The learning rate of the optimizer

BATCH_SIZE = 64           # The batch size for training
BUFFER_CAPACITY = 10000   # The capacity of the replay buffer

NUM_EPISODES = 500    # The number of episodes to train for


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
        x = self.layer3(x)
        return x


# EPSILON-GREEDY ##############################################################

class EpsilonGreedy:
    def __init__(self,
                 epsilon_start: float,
                 epsilon_min: float,
                 epsilon_decay:float,
                 env: gym.Env,
                 q_network: torch.nn.Module):
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.env = env
        self.q_network = q_network

    def __call__(self, state: np.ndarray) -> np.int64:
        """Select action with epsilon-greedy policy"""

        if random.random() < self.epsilon:
            action = self.env.action_space.sample()
        else:
            with torch.no_grad():
                # Convert the state to a PyTorch tensor and add a batch dimension (unsqueeze)
                state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)

                q_values = self.q_network(state_tensor)
                action = q_values.argmax().item()

        return action

    def decay_epsilon(self):
        """Decay epsilon"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)


# REPLAY BUFFER ###############################################################

class ReplayBuffer:
    def __init__(self, capacity: int):
        """Initializes a ReplayBuffer instance

        Args:
            capacity (int): the number of transitions to store in the buffer
        """
        self.buffer = collections.deque(maxlen=capacity)

    def add(self, state: np.ndarray, action: np.int64, reward: float, next_state: np.ndarray, done: bool):
        """Adds a transition to the buffer

        Args:
            state (np.ndarray): the state vector of the added transition
            action (np.int64): the action of the added transition
            reward (float): the reward of the added transition
            next_state (np.ndarray): the next state vector of the added transition
            done (bool): the final state of the added transition
        """
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int) -> Tuple[np.ndarray, float, float, np.ndarray, bool]:
        """Returns a batch of transitions sampled from the buffer.

        Args:
            batch_size (int): the number of transitions to sample

        Returns:
            Tuple[np.ndarray, float, float, np.ndarray, bool]: a batch of `batch_size` transitions
        """
        # Here, `random.sample(self.buffer, batch_size)`
        # returns a list of tuples `(state, action, reward, next_state, done)`
        # where:
        # - `state`  and `next_state` are numpy arrays
        # - `action` and `reward` are floats
        # - `done` is a boolean
        #
        # `states, actions, rewards, next_states, dones = zip(*random.sample(self.buffer, batch_size))`
        # generates 5 tuples `state`, `action`, `reward`, `next_state` and `done`, each having `batch_size` elements.
        states, actions, rewards, next_states, dones = zip(*random.sample(self.buffer, batch_size))
        return np.array(states), actions, rewards, np.array(next_states), dones

    def __len__(self):
        return len(self.buffer)


# TRAINING ####################################################################

def train():

    # SET UP THE ENVIRONMENT

    env = gym.make(GYM_ENVIRONMENT_NAME)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n.item()

    # INITIALIZE AIM

    aim_run = aim.Run(experiment=AIM_EXPERIMENT_NAME)

    # LOG PARAMETERS WITH AIM

    aim_run["hparams"] = {
        "environment_name": GYM_ENVIRONMENT_NAME,
        "nn_l1": NN_L1,
        "nn_l2": NN_L2,
        "gamma": GAMMA,
        "learning_rate": LR,
        "epsilon_start": EPSILON_START,
        "epsilon_min": EPSILON_MIN,
        "epsilon_decay": EPSILON_DECAY,
        "learning_rate": LR,
        "num_episodes": NUM_EPISODES,
        "state_dim": state_dim,
        "action_dim": action_dim,
    }

    print("\n\n" + "*"*80)
    print("Type this in another therminal: aim up")
    print("and open in your web browser the printed URL (e.g. http://127.0.0.1:43800/)")
    print("*"*80, "\n\n")

    # INSTANTIATE REQUIRED OBJECTS

    q_network = QNetwork(state_dim, action_dim).to(device)
    optimizer = torch.optim.AdamW(q_network.parameters(), lr=LR, amsgrad=True)
    loss_fn = torch.nn.MSELoss()

    epsilon_greedy = EpsilonGreedy(EPSILON_START, EPSILON_MIN, EPSILON_DECAY, env, q_network)

    replay_buffer = ReplayBuffer(BUFFER_CAPACITY)

    # TRAINING LOOP

    iteration = 0

    for episode_index in range(NUM_EPISODES):
        state, info = env.reset()
        episode_reward = 0

        for t in itertools.count():

            # GET ACTION, NEXT_STATE AND REWARD ###########

            action = epsilon_greedy(state)

            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            replay_buffer.add(state, action, reward, next_state, done)

            episode_reward += reward

            # UPDATE THE Q_NETWORK WEIGHTS WITH A BATCH OF EXPERIENCES FROM THE BUFFER

            if len(replay_buffer) > BATCH_SIZE:
                batch_states, batch_actions, batch_rewards, batch_next_states, batch_dones = replay_buffer.sample(BATCH_SIZE)

                # Convert to PyTorch tensors
                batch_states_tensor = torch.tensor(batch_states, dtype=torch.float32, device=device)
                batch_actions_tensor = torch.tensor(batch_actions, dtype=torch.long, device=device)
                batch_rewards_tensor = torch.tensor(batch_rewards, dtype=torch.float32, device=device)
                batch_next_states_tensor = torch.tensor(batch_next_states, dtype=torch.float32, device=device)
                batch_dones_tensor = torch.tensor(batch_dones, dtype=torch.float32, device=device)

                # Compute the target Q values for the batch
                with torch.no_grad():
                    # Here's a breakdown of the next line of code:
                    # - `q_network(batch_next_states_t)`:
                    #   This is passing a batch of "next states" through the Q-network.
                    #   This outputs the Q-value for each possible action, a tensor of shape (batch_size, action_dim).
                    #
                    #  - `.max(dim=1)`:
                    #   This is finding the maximum Q-value for each state in the batch.
                    #   The dim=1 argument specifies that the maximum should be taken over the action dimension.
                    #
                    # The max() function in PyTorch returns a tuple containing two tensors: the maximum values and the indices where these maximum values were found.
                    # In the next lines of code, we will just use the first tensor (the maximum values) and ignoring the second tensor (the indices).
                    next_state_q_values, best_action_index = q_network(batch_next_states_tensor).max(dim=1)

                    # The targets for the batch are the rewards plus the discounted maximum Q-values obtained from the next states.
                    # The expression `(1 - batch_dones_tensor)` is used to handle the end of episodes.
                    # The `batch_dones_tensor` indicates whether each state in the batch is a terminal state (i.e., the end of an episode).
                    # If a state is a terminal state, the corresponding value in `batch_dones_tensor` is 1, otherwise it's 0.
                    # The Q-value of a terminal state is defined to be 0. Therefore, when calculating the target Q-values,
                    # we don't want to include the Q-value of the next state if the current state is a terminal state.
                    # This is achieved by multiplying `next_state_q_values` by `(1 - batch_dones_tensor)`.
                    # If the state is a terminal state, this expression becomes 0 and the Q-value of the next state is effectively ignored.
                    # If the state is not a terminal state, this expression is 1 and the Q-value of the next state is included in the calculation.
                    targets = batch_rewards_tensor + GAMMA * next_state_q_values * (1 - batch_dones_tensor)

                # Compute the current Q values for the batch.
                # 
                # The expression `gather(dim=1, index=batch_actions_tensor.unsqueeze(-1)).squeeze(-1)` is used to select specific elements from the tensor of Q-values returned by the Q-network.
                # 
                # Here's a breakdown of the following line of code:
                # - `q_network(batch_states_tensor)`:
                #   This is passing a batch of states through the Q-network.
                #   For each state, this outputs the Q-value for each possible action.
                #   Thus, `q_network(batch_states_tensor)` returns a tensor of shape (batch_size, action_dim).
                # 
                # - `gather(dim=1, index=batch_actions_tensor.unsqueeze(-1))`:
                #   This is selecting the Q-values corresponding to the actions that were actually taken.
                #   The `gather` function is used to select elements from a tensor using an index.
                #   In this case, the index is `batch_actions_tensor.unsqueeze(-1)`, which is a tensor of the actions that were taken.
                #   The `unsqueeze(-1)` function is used to add an extra dimension to the tensor, which is necessary for the `gather` function.
                # 
                # - `squeeze(-1)`:
                #   This is removing the extra dimension that was added by `unsqueeze(-1)`.
                #   The `squeeze` function is used to remove dimensions of size 1 from a tensor.
                #
                # So, the entire expression is selecting the Q-values of the actions that were actually taken from the tensor of all Q-values,
                # and returning a tensor of these selected Q-values.
                current_q_values = q_network(batch_states_tensor).gather(dim=1, index=batch_actions_tensor.unsqueeze(-1)).squeeze(-1)

                # Compute loss
                loss = loss_fn(current_q_values, targets)

                aim_run.track(loss, name='loss', step=iteration, context={ "subset": "train", "type": "loss_type" })

                # Optimize the model
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()


            # LOGS ########################################

            iteration += 1

            if AIM_TRACK_WEIGHTS:
                aim.pytorch.track_params_dists(q_network, aim_run)

            if AIM_TRACK_GRADIENTS:
                aim.pytorch.track_gradients_dists(q_network, aim_run)

            if done:
                print(f"Episode {episode_index+1}/{NUM_EPISODES}: duration={episode_reward}")
                aim_run.track(episode_reward, name='episode_reward', step=episode_index, context={ "subset": "train", "type": "metric_type" })
                aim_run.track(epsilon_greedy.epsilon, name='epsilon', step=episode_index, context={ "subset": "train", "type": "meta_params_type" })
                break

            # UPDATE THE STATE ############################

            state = next_state

        epsilon_greedy.decay_epsilon()


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
    epsilon_greedy = EpsilonGreedy(EPSILON_MIN, EPSILON_MIN, 1., env, q_network)

    # EPISODES LOOP

    while True:
        state, info = env.reset()
        done = False
        episode_reward = 0

        while not done:
            action = epsilon_greedy(state)

            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            episode_reward += reward

            state = next_state

        print(f"Episode reward: {episode_reward}")

    #env.close()


###############################################################################

def main():
    if DO_TRAINING:
        train()

    if DO_INFERENCE:
        inference()

if __name__ == '__main__':
    main()