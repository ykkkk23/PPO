import gymnasium as gym
import torch.nn as nn
import torch


class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.linear1 = nn.Linear(4, 64)
        self.linear2 = nn.Linear(64, 2)

        self.relu = nn.ReLU()
        self.softmax = nn.Softmax()

    def forward(self, x):
        out = self.relu(self.linear1(x))
        out = self.softmax(self.linear2(out))
        return out
    
    def p(self, observation):
        act_mat = self.forward(torch.from_numpy(observation))
        action = torch.multinomial(act_mat, num_samples=1, replacement=True).item()
        return action, act_mat
    

class ValueNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.linear1 = nn.Linear(4, 64)
        self.linear2 = nn.Linear(64, 1)

        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.relu(self.linear1(x))
        out = self.linear2(out)
        return out

    def v(self, x):
        out = self.forward(torch.from_numpy(x))
        return out
    

env = gym.make('CartPole-v1')
obs, _ = env.reset()

# Setup
policy_net = PolicyNet()
value_net = ValueNet()
episodes = 10


for ep in range(episodes):

    total_rew = 0

    while True:
        
        action, act_mat = policy_net.p(obs)
        value = value_net.v(obs)

        obs, rew, terminated, truncated, info = env.step(action)
        total_rew += rew

        if terminated or truncated:
            observation, info = env.reset()
            print(f'episode : {ep + 1} | total reward : {total_rew}')
            break
            
