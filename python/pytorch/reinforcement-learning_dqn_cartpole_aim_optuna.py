#!/usr/bin/env python3
# coding: utf-8

"""
Reinforcement Learning with Vanilla DQN (Deep Q-Network)

Notes: this naive implementation does't use buffer replay and target network.
       Thus, it has very little chance to actually solve the CartPole-v1 problem!
       This is just a base used to build more advanced implementations.
"""

import aim
import aim.pytorch
import gymnasium as gym
import itertools
import numpy as np
import optuna
import random
import torch


# PARAMETERS ###################################################################

GYM_ENVIRONMENT_NAME = "CartPole-v1"
PTH_FILE_NAME = "dqn_cartpole.pth"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# AIM PARAMETERS

AIM_EXPERIMENT_NAME = "reinforcement-learning_dqn_cartpole_optuna"
AIM_TRACK_WEIGHTS = False
AIM_TRACK_GRADIENTS = False

# OPTUNA PARAMETERS

OPTUNA_STUDY_NAME = AIM_EXPERIMENT_NAME + "_with_lr_decay"
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
    
    def __call__(self, state: np.ndarray):
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


# TRAINING ####################################################################

def train(trial):

    # TRAINING PARAMETERS

    NN_L1 = trial.suggest_int('nn_l1', 32, 1024)                     # The number of neurons in the first layer
    NN_L2 = trial.suggest_int('nn_l2', 32, 1024)                     # The number of neurons in the second layer

    GAMMA = trial.suggest_float('gamma', 0.5, 0.99)                  # The discount factor
    EPSILON_START = trial.suggest_float('epsilon_start', 0.1, 0.9)
    EPSILON_MIN = 0.001                                              # The minimum value of epsilon
    EPSILON_DECAY = trial.suggest_float('epsilon_decay', 0.1, 0.999) # The decay rate of epsilon
    LR = trial.suggest_float('lr', 1e-6, 1e-1)                       # The learning rate of the optimizer
    LR_DECAY = trial.suggest_float('lr_decay', 0.1, 0.999)           # The decay rate of epsilon

    NUM_EPISODES = trial.suggest_int('num_episodes', 200, 2000)      # The number of episodes to train for


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
        "learning_rate_decay": LR_DECAY,
        "num_episodes": NUM_EPISODES,
        "state_dim": state_dim,
        "action_dim": action_dim,
    }

    # INSTANTIATE REQUIRED OBJECTS

    q_network = QNetwork(state_dim, action_dim, NN_L1, NN_L2).to(device)
    optimizer = torch.optim.AdamW(q_network.parameters(), lr=LR, amsgrad=True)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=LR_DECAY)
    loss_fn = torch.nn.MSELoss()

    epsilon_greedy = EpsilonGreedy(EPSILON_START, EPSILON_MIN, EPSILON_DECAY, env, q_network)

    # TRAINING LOOP

    iteration = 0
    episode_reward_list = []

    for episode_index in range(NUM_EPISODES):
        state, info = env.reset()
        episode_reward = 0

        for t in itertools.count():

            # GET ACTION, NEXT_STATE AND REWARD ###########

            action = epsilon_greedy(state)

            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            episode_reward += reward

            # UPDATE THE Q_NETWORK WEIGHTS ################

            with torch.no_grad():
                # Convert the next_state to a PyTorch tensor and add a batch dimension (unsqueeze)
                next_state_tensor = torch.tensor(next_state, dtype=torch.float32, device=device).unsqueeze(0)
                target = reward + GAMMA * q_network(next_state_tensor).max()

            # Convert the state to a PyTorch tensor and add a batch dimension (unsqueeze)
            state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
            q_values = q_network(state_tensor)
            q_value_of_current_action = q_values[0, action]

            loss = loss_fn(q_value_of_current_action, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # LOGS ########################################

            iteration += 1
            aim_run.track(loss, name='loss', step=iteration, context={ "subset": "train", "type": "loss_type" })

            if AIM_TRACK_WEIGHTS:
                aim.pytorch.track_params_dists(q_network, aim_run)

            if AIM_TRACK_GRADIENTS:
                aim.pytorch.track_gradients_dists(q_network, aim_run)

            if done:
                #print(f"Episode {episode_index+1}/{NUM_EPISODES}: duration={episode_reward}")
                aim_run.track(episode_reward, name='episode_reward', step=episode_index, context={ "subset": "train", "type": "metric_type" })
                aim_run.track(epsilon_greedy.epsilon, name='epsilon', step=episode_index, context={ "subset": "train", "type": "meta_params_type" })
                aim_run.track(scheduler.get_last_lr()[0], name='learning_rate', step=episode_index, context={ "subset": "train", "type": "meta_params_type" })
                break

            # UPDATE THE STATE ############################

            state = next_state

        episode_reward_list.append(episode_reward)
        epsilon_greedy.decay_epsilon()
        scheduler.step()

    # SAVE THE ACTION-VALUE ESTIMATION FUNCTION ###############################

    torch.save(q_network, PTH_FILE_NAME)

    del q_network   # Remove to demonstrate saving and loading
    env.close()

    # TODO: run N times the trained model and log the average reward
    episode_reward_avg = np.mean(episode_reward_list[-OPTUNA_FITNESS_NUM_TIMESTEPS_AGGREGATED:])

    return episode_reward_avg


# HYPER PARAMETER OPTIMIZATION ################################################

def optuna_objective_fn(trial):
    episode_reward_avg_list = []

    for training_index in range(OPTUNA_NUM_TRAININGS_PER_TRIAL):
        episode_reward_avg = train(trial)
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