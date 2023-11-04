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
import optuna
import random
import torch
from typing import Tuple


# PARAMETERS ###################################################################

GYM_ENVIRONMENT_NAME = "CartPole-v1"
PTH_FILE_NAME = "dqn_cartpole.pth"

VERBOSE = False

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# AIM PARAMETERS

AIM_EXPERIMENT_NAME = "reinforcement-learning_dqn_cartpole_optuna"
AIM_TRACK_WEIGHTS = False
AIM_TRACK_GRADIENTS = False

# OPTUNA PARAMETERS

OPTUNA_STUDY_NAME = AIM_EXPERIMENT_NAME + "_with_buffer_replay"
OPTUNA_FITNESS_NUM_TIMESTEPS_AGGREGATED = 10
OPTUNA_NUM_TRAININGS_PER_TRIAL = 3
OPTUNA_NUM_TRIALS = 1000
OPTUNA_STORAGE = "sqlite:///optuna_db.sqlite3"


# ACTION-VALUE FUNCTION ESTIMATION ############################################

class QNetwork(torch.nn.Module):

    def __init__(self, n_observations, n_actions, nn_l1, nn_l2):
        super(QNetwork, self).__init__()
        self.layer1 = torch.nn.Linear(n_observations, nn_l1)
        self.layer2 = torch.nn.Linear(nn_l1, nn_l2)
        self.layer3 = torch.nn.Linear(nn_l2, n_actions)

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

def train(nn_l1, nn_l2, gamma, epsilon_start, epsilon_min, epsilon_decay, lr, lr_decay, batch_size, buffer_capacity, num_episodes):

    # SET UP THE ENVIRONMENT

    env = gym.make(GYM_ENVIRONMENT_NAME)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n.item()

    # INITIALIZE AIM

    aim_run = aim.Run(experiment=AIM_EXPERIMENT_NAME)

    # LOG PARAMETERS WITH AIM

    aim_run["hparams"] = {
        "environment_name": GYM_ENVIRONMENT_NAME,
        "nn_l1": nn_l1,
        "nn_l2": nn_l2,
        "gamma": gamma,
        "learning_rate": lr,
        "epsilon_start": epsilon_start,
        "epsilon_min": epsilon_min,
        "epsilon_decay": epsilon_decay,
        "learning_rate": lr,
        "learning_rate_decay": lr_decay,
        "num_episodes": num_episodes,
        "state_dim": state_dim,
        "action_dim": action_dim,
    }

    # INSTANTIATE REQUIRED OBJECTS

    q_network = QNetwork(state_dim, action_dim, nn_l1, nn_l2).to(device)
    optimizer = torch.optim.AdamW(q_network.parameters(), lr=lr, amsgrad=True)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=lr_decay)
    loss_fn = torch.nn.MSELoss()

    epsilon_greedy = EpsilonGreedy(epsilon_start, epsilon_min, epsilon_decay, env, q_network)

    replay_buffer = ReplayBuffer(buffer_capacity)

    # TRAINING LOOP

    iteration = 0
    episode_reward_list = []

    for episode_index in range(num_episodes):
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

            if len(replay_buffer) > batch_size:
                batch_states, batch_actions, batch_rewards, batch_next_states, batch_dones = replay_buffer.sample(batch_size)

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
                    targets = batch_rewards_tensor + gamma * next_state_q_values * (1 - batch_dones_tensor)

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
                scheduler.step()


            # LOGS ########################################

            iteration += 1

            if AIM_TRACK_WEIGHTS:
                aim.pytorch.track_params_dists(q_network, aim_run)

            if AIM_TRACK_GRADIENTS:
                aim.pytorch.track_gradients_dists(q_network, aim_run)

            if done:
                if VERBOSE:
                    print(f"Episode {episode_index+1}/{num_episodes}: duration={episode_reward}")
                aim_run.track(episode_reward, name='episode_reward', step=episode_index, context={ "subset": "train", "type": "metric_type" })
                aim_run.track(epsilon_greedy.epsilon, name='epsilon', step=episode_index, context={ "subset": "train", "type": "meta_params_type" })
                aim_run.track(scheduler.get_last_lr()[0], name='learning_rate', step=episode_index, context={ "subset": "train", "type": "meta_params_type" })
                break

            # UPDATE THE STATE ############################

            state = next_state

        episode_reward_list.append(episode_reward)
        epsilon_greedy.decay_epsilon()


    # SAVE THE ACTION-VALUE ESTIMATION FUNCTION ###############################

    torch.save(q_network, PTH_FILE_NAME)

    del q_network   # Remove to demonstrate saving and loading
    env.close()

    return episode_reward_list


# HYPER PARAMETER OPTIMIZATION ################################################

def optuna_objective_fn(trial):

    # TRAINING PARAMETERS #################################

    hyper_params = {
        "nn_l1": trial.suggest_int('nn_l1', 32, 1024),                       # The number of neurons in the first layer
        "nn_l2": trial.suggest_int('nn_l2', 32, 1024),                       # The number of neurons in the second layer
        "gamma": trial.suggest_float('gamma', 0.5, 0.99),                    # The discount factor
        "epsilon_start": trial.suggest_float('epsilon_start', 0.1, 0.9),
        "epsilon_min": 0.001,                                                # The minimum value of epsilon
        "epsilon_decay": trial.suggest_float('epsilon_decay', 0.1, 0.999),   # The decay rate of epsilon
        "lr": trial.suggest_float('lr', 1e-6, 1e-1),                         # The learning rate of the optimizer
        "lr_decay": trial.suggest_float('lr_decay', 0.1, 0.999),             # The decay rate of epsilon
        "batch_size": trial.suggest_int('batch_size', 32, 128),              # The batch size for training
        "buffer_capacity": trial.suggest_int('buffer_capacity', 100, 2000),  # The capacity of the replay buffer
        "num_episodes": trial.suggest_int('num_episodes', 200, 2000),        # The number of episodes to train for
    }

    # HYPER PARAMETER OPTIMIZATION LOOP ###################

    episode_reward_avg_list = []

    for training_index in range(OPTUNA_NUM_TRAININGS_PER_TRIAL):
        episode_reward_list = train(**hyper_params)
        episode_reward_avg = np.mean(episode_reward_list[-OPTUNA_FITNESS_NUM_TIMESTEPS_AGGREGATED:])
        episode_reward_avg_list.append(episode_reward_avg)

    return np.mean(episode_reward_avg_list)


###############################################################################

def main():

    # PRINT AIM INSTRUCTIONS ##############################

    print("\n\n" + "*"*80)
    print("Type this in another therminal: aim up")
    print("and open in your web browser the printed URL (e.g. http://127.0.0.1:43800/)")
    print("*"*80, "\n\n")

    # OPTUNA HYPER PARAMETER OPTIMIZATION #################

    # study = optuna.create_study(direction='maximize')
    # study.optimize(train, n_trials=10)

    study = optuna.create_study(direction='maximize', storage=OPTUNA_STORAGE, study_name=OPTUNA_STUDY_NAME, load_if_exists=True)
    study.optimize(optuna_objective_fn, n_trials=OPTUNA_NUM_TRIALS)

    print(f"Best value: {study.best_value} (params: {study.best_params})")


if __name__ == '__main__':
    main()