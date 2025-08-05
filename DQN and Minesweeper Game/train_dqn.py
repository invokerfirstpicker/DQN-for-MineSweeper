import numpy as np
from minesweeper_env import MinesweeperEnv
from dqn_agent import DQNAgent
import os
import time

# Настройки
EPISODES = 10000
SAVE_EVERY = 500
MODEL_PATH = 'dqn_weights.pth'
VISUALIZE_EVERY = 500  # как часто показывать игру агента

# Создаём среду и агента
env = MinesweeperEnv()
state_shape = env.observation_space
n_actions = env.action_space
agent = DQNAgent(state_shape, n_actions)

# Если есть сохранённая модель — загружаем
if os.path.exists(MODEL_PATH):
    print('Загружаю сохранённую модель...')
    agent.load(MODEL_PATH)

for episode in range(1, EPISODES + 1):
    state = env.reset()
    done = False
    total_reward = 0
    steps = 0
    while not done:
        # Преобразуем состояние для агента
        state_input = state.astype(np.float32) / 8.0  # нормализация
        action = agent.select_action(state_input)
        next_state, reward, done, info = env.step(action)
        next_state_input = next_state.astype(np.float32) / 8.0
        agent.store(state_input, action, reward, next_state_input, done)
        agent.update()
        state = next_state
        total_reward += reward
        steps += 1
    # Лог
    print(f"Эпизод {episode}: шагов {steps}, награда {total_reward:.2f}, epsilon {agent.epsilon:.3f}")
    if episode % SAVE_EVERY == 0:
        agent.save(MODEL_PATH)
        print(f"Модель сохранена в {MODEL_PATH}")
    # Визуализация игры агента
    if episode % VISUALIZE_EVERY == 0:
        print("\nВизуализация: агент играет одну партию...")
        vis_env = MinesweeperEnv()
        vis_state = vis_env.reset()
        vis_done = False
        vis_steps = 0
        while not vis_done:
            vis_env.render()
            vis_state_input = vis_state.astype(np.float32) / 8.0
            vis_action = agent.select_action(vis_state_input)
            vis_state, vis_reward, vis_done, vis_info = vis_env.step(vis_action)
            vis_steps += 1
            time.sleep(0.1)  # задержка для наглядности
        vis_env.render()
        if 'win' in vis_info:
            print(f'Агент победил за {vis_steps} ходов!')
        elif 'lose' in vis_info:
            print(f'Агент проиграл за {vis_steps} ходов!')
        print("---\n")

# Финальное сохранение
agent.save(MODEL_PATH)
print('Обучение завершено, модель сохранена!')