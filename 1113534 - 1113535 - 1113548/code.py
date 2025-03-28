# -*- coding: utf-8 -*-
"""Untitled19.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19kDOW_ceiqkzR8VBxZlnVNFoPmdRy_X6

Import Libraries and Define Initial Parameters
"""

# Cell to Import Libraries and Define Initial Parameters
!pip install gym # a toolkit for developing and comparing reinforcement learning algorithms.
!pip install stable-baselines3[extra] # collection of popular reinforcement learning algorithms.
!pip install 'shimmy>=2.0'

!pip install scikit-learn # used for machine learning tasks such as data preprocessing, modeling, and evaluation.

"""Data Generation and Preprocessing"""

# Cell for Data Generation and Preprocessing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split # For splitting the dataset into training and testing sets
from sklearn.preprocessing import StandardScaler # For standardizing features to have a mean of 0 and variance of 1
from imblearn.over_sampling import SMOTE # For handling imbalanced datasets using Synthetic Minority Over-sampling Technique
from collections import Counter # For counting occurrences of class labels

# Seed for reproducibility
np.random.seed(0)

# Generate synthetic data
num_data = 1000 # Number of data points to generate
data = {
    'temperature': np.random.normal(50, 10, num_data),
    'vibration': np.random.normal(0.5, 0.1, num_data),
    'operational_hours': np.random.normal(10, 2, num_data),
    'failure': np.random.binomial(1, 0.1, num_data) # Binary failure status with a 10% probability of failure
}
df = pd.DataFrame(data)

# Add new features to track changes in temperature and vibration
df['temp_change'] = df['temperature'].diff().fillna(0)
df['vib_change'] = df['vibration'].diff().fillna(0)


# Feature scaling and data splitting
features = df[['temperature', 'vibration', 'operational_hours', 'temp_change', 'vib_change']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(scaled_features, df['failure'], test_size=0.2, random_state=0)

# Apply SMOTE to balance the training set
smote = SMOTE(random_state=0)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Verify class distribution
print(f"Original class distribution: {Counter(y_train)}")
print(f"Resampled class distribution: {Counter(y_resampled)}")

"""Define the EquipementEnv Class"""

import gym  # Import the gym module
from gym import spaces  # Import spaces from gym
import numpy as np

class EquipmentEnv(gym.Env):
    """Custom Environment that follows gym interface."""
    metadata = {'render.modes': ['human']}

    def __init__(self, data, labels):
        super(EquipmentEnv, self).__init__()
        self.data = data  # Assuming data is a DataFrame, convert to numpy for consistent indexing
        self.labels = labels.values  # Convert labels to numpy array to avoid indexing issues
        self.index = 0
        self.action_space = spaces.Discrete(2)  # Binary actions: 0 (no maintenance) or 1 (maintenance)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(data.shape[1],), dtype=np.float32
        )

    def step(self, action):
        """Perform a step in the environment."""
        self.index += 1  # Move to the next index
        done = self.index >= len(self.data)  # Check if we reached the end of the data

        # Initialize the reward
        reward = 0

        # Only calculate rewards if the episode is not done
        if not done:
            if action == 1 and self.labels[self.index] == 1:
                reward = 50  # Reward for correct maintenance
            elif action == 0 and self.labels[self.index] == 0:
                reward = 5  # Reward for correctly avoiding maintenance
            elif action == 1 and self.labels[self.index] == 0:
                reward = -1  # Penalty for unnecessary maintenance
            elif action == 0 and self.labels[self.index] == 1:
                reward = -12  # Penalty for missing required maintenance

            # Print to track rewards and actions
            print(f"Step {self.index}: Action={action}, Label={self.labels[self.index]}, Reward={reward}")

        # Prepare the next state or a zeroed state if the episode is done
        next_state = (
            self.data[self.index] if not done else np.zeros(self.observation_space.shape)
        )

        # Return the step information
        info = {}
        return next_state, reward, done, info

    def reset(self):
        """Reset the environment to the initial state."""
        self.index = np.random.randint(0, len(self.data) - 1)  # Randomize the initial state
        print(f"Environment reset. Starting index: {self.index}")
        return self.data[self.index]

    def render(self, mode='human', close=False):
        """Render the current state of the environment."""
        if mode == 'human':
            print(f"Current Index: {self.index}")
        pass

"""Training"""

from stable_baselines3 import PPO

# Create the training environment
env = EquipmentEnv(X_train, y_train)

# Define the PPO model
model = PPO("MlpPolicy", env, verbose=1, ent_coef=0.01)  # Entropy for exploration

# Train the model
model.learn(total_timesteps=10000)

"""Evaluation"""

# Create the evaluation environment
eval_env = EquipmentEnv(X_test, y_test)

# Reset the environment
obs = eval_env.reset()
done = False

# Evaluate the model
while not done:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = eval_env.step(action)
    print(f"Action: {action}, Reward: {reward}")
    if done:
        obs = eval_env.reset()  # Properly reset the environment at the end of an episode

import logging
import sys
import matplotlib.pyplot as plt

# Configure logging to print to console only
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Print to console only
    ]
)

# Store total rewards for visualization
rewards = []

# Training and logging
for episode in range(10):  # Example: Running 10 evaluation episodes
    print(f"Starting episode {episode}")
    logging.info(f"Starting episode {episode}")  # Log start of episode
    state = env.reset()
    total_reward = 0
    done = False
    while not done:
        action, _states = model.predict(state, deterministic=True)
        state, reward, done, _ = env.step(action)
        total_reward += reward
        logging.info(f'Episode: {episode}, Action: {action}, Reward: {reward}')
        print(f'Episode: {episode}, Action: {action}, Reward: {reward}')  # Debug print
    logging.info(f'Total reward for episode {episode}: {total_reward}')
    print(f'Total reward for episode {episode}: {total_reward}')  # Debug print
    rewards.append(total_reward)  # Collect total rewards in the list

# Debug: Check collected rewards
print("Collected rewards:", rewards)

# Plot the rewards
plt.figure(figsize=(10, 5))
plt.plot(range(len(rewards)), rewards, marker='o', linestyle='-', label="Total Reward")
plt.axhline(y=0, color='r', linestyle='--', label="Neutral Reward Level")  # Neutral reward line
plt.title('Total Rewards per Episode')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.legend()
plt.grid(True)
plt.show()

cumulative_rewards = [sum(rewards[:i+1]) for i in range(len(rewards))]

plt.figure(figsize=(10, 5))
plt.plot(range(len(cumulative_rewards)), cumulative_rewards, marker='o', linestyle='-', label="Cumulative Reward")
plt.title('Cumulative Rewards Over Episodes')
plt.xlabel('Episode')
plt.ylabel('Cumulative Reward')
plt.legend()
plt.grid(True)
plt.show()

action_distribution = {0: 0, 1: 0}

for episode in range(10):  #
    obs = eval_env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        action_distribution[int(action)] += 1
        obs, reward, done, _ = eval_env.step(action)

actions = list(action_distribution.keys())
frequencies = list(action_distribution.values())

plt.figure(figsize=(8, 5))
plt.bar(actions, frequencies, color=["blue", "orange"])
plt.title("Action Distribution")
plt.xlabel("Action")
plt.ylabel("Frequency")
plt.xticks([0, 1], ["No Maintenance", "Perform Maintenance"])
plt.grid(axis='y')
plt.show()