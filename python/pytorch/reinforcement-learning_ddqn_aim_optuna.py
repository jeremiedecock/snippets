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

TASK = "meta_params_optimization"
# TASK = "train"
# TASK = "inference"

GYM_ENVIRONMENT_NAME = "CartPole-v1"
#GYM_ENVIRONMENT_NAME = "LunarLander-v2"
#GYM_ENVIRONMENT_NAME = "CarRacing-v2"

if GYM_ENVIRONMENT_NAME == "CarRacing-v2":
    GYM_ENVIRONMENT_PARAMS = {"continuous": False}
else:
    GYM_ENVIRONMENT_PARAMS = {}

PTH_FILE_NAME = f"dqn_{ GYM_ENVIRONMENT_NAME.lower() }.pth"

VERBOSE = False

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# AIM PARAMETERS ######################

AIM_EXPERIMENT_NAME = f"reinforcement-learning_ddqn_{ GYM_ENVIRONMENT_NAME.lower() }"
AIM_TRACK_WEIGHTS = False
AIM_TRACK_GRADIENTS = False


# OPTUNA PARAMETERS ###################

OPTUNA_STUDY_NAME = AIM_EXPERIMENT_NAME
OPTUNA_FITNESS_NUM_TIMESTEPS_AGGREGATED = 50
OPTUNA_NUM_TRAININGS_PER_TRIAL = 5
OPTUNA_NUM_TRIALS = 1000
OPTUNA_STORAGE = "sqlite:///optuna_db.sqlite3"

HYPER_PARAMS = {
    "batch_size": (128, 128),                  # The batch size for training
    "buffer_capacity": (1000, 10000),           # The capacity of the replay buffer
    "clip_grad_value": (10, 100),            # The maximum value of the gradient
    "epsilon_start": (0.5, 0.9),
    "epsilon_min": (0.001, 0.1),            # The minimum value of epsilon
    "epsilon_decay": (0.9, 0.9999),            # The decay rate of epsilon
    "gamma": (0.9, 0.9),                     # The discount factor
    "lr": (1e-5, 1e-2),                       # The learning rate of the optimizer
    "lr_decay": (0.9, 0.9999),                 # The decay rate of epsilon
    "nn_l1": (128, 128),                      # The number of neurons in the first layer
    "nn_l2": (128, 128),                      # The number of neurons in the second layer
    "num_episodes": (150, 150),              # The number of episodes to train for
    "target_q_network_sync_period": (10, 100), # The number of training steps between each update of the target Q-network
}


# TRAINING PARAMETERS #################

# SIMO

# NN_L1 = 1024                        # The number of neurons in the first layer
# NN_L2 = 512                        # The number of neurons in the second layer

# GAMMA = 0.95                       # The discount factor
# EPSILON_START = 1.0                # The starting value of epsilon
# EPSILON_MIN = 0.001                # The minimum value of epsilon
# EPSILON_DECAY = 0.999              # The decay rate of epsilon
# LR = 1e-4                          # The learning rate of the optimizer
# LR_DECAY = 1.                      # The decay rate of the learning rate

# BATCH_SIZE = 64                    # The batch size for training
# BUFFER_CAPACITY = 10000            # The capacity of the replay buffer

# TARGET_Q_NETWORK_SYNC_PERIOD = 10  # The number of training steps between each update of the target Q-network
# CLIP_GRAD_VALUE = 100.             # The maximum value of the gradient

# NUM_EPISODES = 150                 # The number of episodes to train for




# NN_L1 = 861                        # The number of neurons in the first layer
# NN_L2 = 961                        # The number of neurons in the second layer

# GAMMA = 0.8865193527159189                       # The discount factor
# EPSILON_START = 0.6179386474434864                # The starting value of epsilon
# EPSILON_MIN = 0.001                # The minimum value of epsilon
# EPSILON_DECAY = 0.35718755799558033              # The decay rate of epsilon
# LR = 0.05687621727630155                          # The learning rate of the optimizer
# LR_DECAY = 0.9984026100428682                      # The decay rate of the learning rate

# BATCH_SIZE = 103                    # The batch size for training
# BUFFER_CAPACITY = 240            # The capacity of the replay buffer

# TARGET_Q_NETWORK_SYNC_PERIOD = 5  # The number of training steps between each update of the target Q-network
# CLIP_GRAD_VALUE = 6.277941356549787             # The maximum value of the gradient

# NUM_EPISODES = 1165                 # The number of episodes to train for


# # MY BEST SO FAR
# NN_L1 = 128                        # The number of neurons in the first layer
# NN_L2 = 128                        # The number of neurons in the second layer

# GAMMA = 0.9                       # The discount factor

# EPSILON_START = 0.6                # The starting value of epsilon
# EPSILON_MIN = 0.05                # The minimum value of epsilon
# EPSILON_DECAY = 0.9              # The decay rate of epsilon

# LR = 0.05                          # The learning rate of the optimizer
# LR_MIN = 0.0001
# LR_DECAY = 0.999                      # The decay rate of the learning rate

# BATCH_SIZE = 128                    # The batch size for training
# BUFFER_CAPACITY = 1000            # The capacity of the replay buffer

# TARGET_Q_NETWORK_SYNC_PERIOD = 10  # The number of training steps between each update of the target Q-network
# CLIP_GRAD_VALUE = 5.             # The maximum value of the gradient

# NUM_EPISODES = 100                 # The number of episodes to train for


NN_L1 = 128                        # The number of neurons in the first layer
NN_L2 = 128                        # The number of neurons in the second layer

GAMMA = 0.9                       # The discount factor

EPSILON_START = 0.6                # The starting value of epsilon
EPSILON_MIN = 0.05                # The minimum value of epsilon
EPSILON_DECAY = 0.99              # The decay rate of epsilon

LR = 0.01                          # The learning rate of the optimizer
LR_MIN = 0.0001
LR_DECAY = 0.999                      # The decay rate of the learning rate

BATCH_SIZE = 128                    # The batch size for training
BUFFER_CAPACITY = 10000            # The capacity of the replay buffer

TARGET_Q_NETWORK_SYNC_PERIOD = 100  # The number of training steps between each update of the target Q-network
CLIP_GRAD_VALUE = 100.             # The maximum value of the gradient

NUM_EPISODES = 500                 # The number of episodes to train for


# TUTO PYTORCH

# NN_L1 = 128                        # The number of neurons in the first layer
# NN_L2 = 128                        # The number of neurons in the second layer

# GAMMA = 0.99                       # The discount factor
# EPSILON_START = 0.9                # The starting value of epsilon
# EPSILON_MIN = 0.05                # The minimum value of epsilon
# EPSILON_DECAY =               # The decay rate of epsilon
# LR = 1e-4                          # The learning rate of the optimizer
# LR_DECAY =                       # The decay rate of the learning rate

# BATCH_SIZE = 128                    # The batch size for training
# BUFFER_CAPACITY = 10000            # The capacity of the replay buffer

# TARGET_Q_NETWORK_SYNC_PERIOD =   # The number of training steps between each update of the target Q-network
# CLIP_GRAD_VALUE = 100             # The maximum value of the gradient

# NUM_EPISODES = 600                 # The number of episodes to train for


# INFERENCE PARAMETERS ################

EPSILON = 0.001


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


# LEARNING RATE SCHEDULER #####################################################

class MinimumExponentialLR(torch.optim.lr_scheduler.ExponentialLR):
    def __init__(self, optimizer, gamma, last_epoch=-1, min_lr=1e-6):
        self.min_lr = min_lr
        super().__init__(optimizer, gamma, last_epoch=-1)

    def get_lr(self):
        return [
            max(base_lr * self.gamma ** self.last_epoch, self.min_lr)
            for base_lr in self.base_lrs
        ]


# TRAINING ####################################################################

def train(nn_l1, nn_l2, gamma, epsilon_start, epsilon_min, epsilon_decay, lr, lr_decay, batch_size, buffer_capacity, num_episodes, target_q_network_sync_period, clip_grad_value):

    # SET UP THE ENVIRONMENT

    env = gym.make(GYM_ENVIRONMENT_NAME, **GYM_ENVIRONMENT_PARAMS)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n.item()

    # INITIALIZE AIM

    aim_run = aim.Run(experiment=AIM_EXPERIMENT_NAME)

    # LOG PARAMETERS WITH AIM

    aim_run["hparams"] = {
        "action_dim": action_dim,
        "batch_size": batch_size,
        "buffer_capacity": buffer_capacity,
        "clip_grad_value": clip_grad_value,
        "environment_name": GYM_ENVIRONMENT_NAME,
        "epsilon_decay": epsilon_decay,
        "epsilon_min": epsilon_min,
        "epsilon_start": epsilon_start,
        "gamma": gamma,
        "learning_rate": lr,
        "learning_rate_decay": lr_decay,
        "nn_l1": nn_l1,
        "nn_l2": nn_l2,
        "num_episodes": num_episodes,
        "state_dim": state_dim,
        "target_q_network_sync_period": target_q_network_sync_period,
    }


    # INSTANTIATE REQUIRED OBJECTS

    q_network = QNetwork(state_dim, action_dim, nn_l1, nn_l2).to(device)
    target_q_network = QNetwork(state_dim, action_dim, nn_l1, nn_l2).to(device) # The target Q-network is used to compute the target Q-values for the loss function
    target_q_network.load_state_dict(q_network.state_dict()) # Initialize the target Q-network with the same weights as the Q-network

    optimizer = torch.optim.AdamW(q_network.parameters(), lr=lr, amsgrad=True)
    #scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=lr_decay)
    scheduler = MinimumExponentialLR(optimizer, gamma=lr_decay, min_lr=LR_MIN)
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
                    next_state_q_values, best_action_index = target_q_network(batch_next_states_tensor).max(dim=1)

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
                torch.nn.utils.clip_grad_value_(q_network.parameters(), clip_grad_value)  # In-place gradient clipping
                optimizer.step()

                scheduler.step()

            # UPDATE THE TARGET Q-NETWORK #################

            # Every few training steps (e.g., every 100 steps), the weights of the target network are updated with the weights of the Q-network

            if iteration % target_q_network_sync_period == 0:
                target_q_network.load_state_dict(q_network.state_dict())

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

    hyper_params = {key: trial.suggest_int(key, *HYPER_PARAMS[key]) for key in HYPER_PARAMS if isinstance(HYPER_PARAMS[key][0], int)}
    hyper_params.update({key: trial.suggest_float(key, *HYPER_PARAMS[key]) for key in HYPER_PARAMS if isinstance(HYPER_PARAMS[key][0], float)})
    # trial.suggest_int("batch_size", *HYPER_PARAMS["batch_size"])
    # trial.suggest_int("buffer_capacity", *HYPER_PARAMS["buffer_capacity"])
    # trial.suggest_int("clip_grad_value", *HYPER_PARAMS["clip_grad_value"])
    # trial.suggest_float("epsilon_start", *HYPER_PARAMS["epsilon_start"])
    # trial.suggest_float("epsilon_min", *HYPER_PARAMS["epsilon_min"])
    # trial.suggest_float("epsilon_decay", *HYPER_PARAMS["epsilon_decay"])
    # trial.suggest_float("gamma", *HYPER_PARAMS["gamma"])
    # trial.suggest_float("lr", *HYPER_PARAMS["lr"])
    # trial.suggest_float("lr_decay", *HYPER_PARAMS["lr_decay"])
    # trial.suggest_int("nn_l1", *HYPER_PARAMS["nn_l1"])
    # trial.suggest_int("nn_l2", *HYPER_PARAMS["nn_l2"])
    # trial.suggest_int("num_episodes", *HYPER_PARAMS["num_episodes"])
    # trial.suggest_int("target_q_network_sync_period", *HYPER_PARAMS["target_q_network_sync_period"])

    # HYPER PARAMETER OPTIMIZATION LOOP ###################

    episode_reward_avg_list = []

    for training_index in range(OPTUNA_NUM_TRAININGS_PER_TRIAL):
        episode_reward_list = train(**hyper_params)
        episode_reward_avg = np.mean(episode_reward_list[-OPTUNA_FITNESS_NUM_TIMESTEPS_AGGREGATED:])
        episode_reward_avg_list.append(episode_reward_avg)

    return np.mean(episode_reward_avg_list)


###############################################################################

def inference(epsilon: float):

    # INSTANTIATE REQUIRED OBJECTS

    env = gym.make(GYM_ENVIRONMENT_NAME, render_mode="human")
    q_network = torch.load(PTH_FILE_NAME).to(device)
    epsilon_greedy = EpsilonGreedy(epsilon, epsilon, 1., env, q_network)

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

    if TASK in ("meta_params_optimization", "train"):
        # PRINT AIM INSTRUCTIONS
        print("\n\n" + "*"*80)
        print("Type this in another therminal: aim up")
        print("and open in your web browser the printed URL (e.g. http://127.0.0.1:43800/)")
        print("*"*80, "\n\n")

    if TASK == "meta_params_optimization":
        study = optuna.create_study(direction='maximize', storage=OPTUNA_STORAGE, study_name=OPTUNA_STUDY_NAME, load_if_exists=True)
        study.optimize(optuna_objective_fn, n_trials=OPTUNA_NUM_TRIALS)

        print(f"Best value: {study.best_value} (params: {study.best_params})")

    elif TASK == "train":
        episode_reward_list = train(NN_L1, NN_L2, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY, LR, LR_DECAY, BATCH_SIZE, BUFFER_CAPACITY, NUM_EPISODES, TARGET_Q_NETWORK_SYNC_PERIOD, CLIP_GRAD_VALUE)
        print(episode_reward_list[-10:])

    elif TASK == "inference":
        inference(EPSILON)

    else:
        raise ValueError(f"Unknown task: {TASK}, must be one of: 'meta_params_optimization', 'train' or 'inference'")


if __name__ == '__main__':
    main()