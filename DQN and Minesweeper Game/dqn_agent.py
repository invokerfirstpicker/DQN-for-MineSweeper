import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

# Простой сверточный Q-Network для сапёра
class QNetwork(nn.Module):
    def __init__(self, input_shape, n_actions):
        super(QNetwork, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * input_shape[0] * input_shape[1], 512),
            nn.ReLU(),
            nn.Linear(512, n_actions)
        )
    def forward(self, x):
        x = x.unsqueeze(1)  # добавляем канал
        x = self.conv(x)
        return self.fc(x)

class DQNAgent:
    def __init__(self, state_shape, n_actions, lr=1e-3, gamma=0.99, epsilon_start=1.0, epsilon_final=0.1, epsilon_decay=10000, buffer_size=50000, batch_size=64):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.q_network = QNetwork(state_shape, n_actions).to(self.device)
        self.target_network = QNetwork(state_shape, n_actions).to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_final = epsilon_final
        self.epsilon_decay = epsilon_decay
        self.n_actions = n_actions
        self.batch_size = batch_size
        self.memory = deque(maxlen=buffer_size)
        self.learn_step = 0

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        state = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_network(state)
        return int(torch.argmax(q_values).item())

    def store(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample_memory(self):
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(dones))

    def update(self):
        if len(self.memory) < self.batch_size:
            return
        states, actions, rewards, next_states, dones = self.sample_memory()
        states = torch.tensor(states, dtype=torch.float32, device=self.device)
        actions = torch.tensor(actions, dtype=torch.int64, device=self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        next_states = torch.tensor(next_states, dtype=torch.float32, device=self.device)
        dones = torch.tensor(dones, dtype=torch.float32, device=self.device)

        q_values = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]
        expected_q = rewards + self.gamma * next_q_values * (1 - dones)
        loss = nn.MSELoss()(q_values, expected_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Обновление epsilon
        self.epsilon = max(self.epsilon_final, self.epsilon - (1.0 - self.epsilon_final) / self.epsilon_decay)
        # Периодически обновляем target-сеть
        self.learn_step += 1
        if self.learn_step % 1000 == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())

    def save(self, path):
        torch.save({
            'q_network': self.q_network.state_dict(),
            'target_network': self.target_network.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon
        }, path)

    def load(self, path):
        checkpoint = torch.load(path, map_location=self.device)
        self.q_network.load_state_dict(checkpoint['q_network'])
        self.target_network.load_state_dict(checkpoint['target_network'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.epsilon = checkpoint['epsilon']