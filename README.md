Deep Reinforcement Learning for Predictive Maintenance
A project that explores how reinforcement learning (RL) can be applied to predictive maintenance by training an agent to make optimal decisions on equipment repair using synthetic industrial data.

📌 Overview
This project uses a custom environment built with OpenAI Gym to simulate equipment operation and failures. A reinforcement learning agent, trained using the Proximal Policy Optimization (PPO) algorithm, learns when to perform maintenance in order to reduce downtime and prevent unnecessary actions.

🚀 Key Features
✅ Custom RL Environment: Simulates predictive maintenance scenarios using sensor-based equipment data.

🧠 PPO Agent: Trained to maximize rewards through correct maintenance decisions.

📊 Synthetic Dataset: Includes temperature, vibration, and operational hour features with failure labels.

📉 Reward Strategy: Balanced to penalize missed maintenance and encourage efficient behavior.

📈 Results Visualization: Includes total reward trends and action distributions.

🔍 Methodology
🧾 Dataset Generation
Synthetic features: Temperature, Vibration, Operational Hours.

Failure labels: 10% probability of failure.

Data balancing: SMOTE used to address class imbalance in training data.

🧠 Environment Design
States: Equipment metrics.

Actions:

0: No maintenance

1: Perform maintenance

Reward Structure:

+50: Correct maintenance

+5: Correct no maintenance

-1: Unnecessary maintenance

-10: Missed maintenance

📊 Model Training
Algorithm: Proximal Policy Optimization (PPO)

Library: Stable-Baselines3

Scaler: StandardScaler for feature normalization

📈 Results
Reward plots showed learning progress over episodes.

Action distributions confirmed balanced decision-making.

Agent avoided unnecessary maintenance while successfully predicting failures.

💡 Future Improvements
Compare with other RL algorithms (e.g., DQN, A2C).

Use real-world industrial datasets.

Optimize reward structures further.

Integrate digital twin or IoT frameworks.

📚 References
Sutton, R. S., & Barto, A. G. Reinforcement Learning: An Introduction

OpenAI Gym: https://www.gymlibrary.dev/

SMOTE: Chawla et al. (2002)

👥 Team
Guerrier Hantz Brunet

古弘恩

Max 田雷西

范瑞德 Arridson
