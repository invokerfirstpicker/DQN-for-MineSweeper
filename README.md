# 🎮 DQN Minesweeper AI

A project to train artificial intelligence to play the classic Minesweeper game using the Deep Q-Network (DQN).

## 📋 Project Description

This project demonstrates the use of deep Reinforcement Learning to create an AI agent capable of playing minesweeper. The agent is trained using the Deep Q-Network algorithm and can play on a 16x16 field with 40 mines.

## 🏗️ Project architecture

``
DQN and Minesweeper Game/
├── ai_minesweeper.py # GUI for demonstrating trained AI
├── minesweeper_env.py # RL-Agent training environment
,── train_dqn.py # DQN Agent training script
├── run_ai_game.py # Launching an AI demonstration
,── minesweeper.py # Classic human game
,── dqn_agent.py # Implementing
the DQN agent ├── requirements.txt # Project dependencies
,── README.md # Documentation
```

## 🚀 Quick Start

### 1. Installing dependencies

```bash
pip install -r requirements.txt
```

### 2. Agent Training

```bash
python train_dqn.py
```

The training will take some time. The model will be saved to the `dqn_weights.pth` file every 500 episodes.

###3. Launching an AI demonstration

```bash
python run_ai_game.py
```

Or directly:

```bash
python ai_minesweeper.py
```

## 🎯 Main components

### 🤖 DQN Agent (`dqn_agent.py `)
- Implementation of the Deep Q-Network agent
- Uses PyTorch for a neural network
- Supports saving/loading of trained models

### 🎮 RL Environment (`minesweeper_env.py `)
is a Gym-compatible learning environment
- State: 16x16 matrix (closed/open cells, numbers)
- Actions: coordinates of the cell to open
- Rewards: +10 for victory, -10 for defeat, +0.1 for each open square

### 🖥️ AI Demo (`ai_minesweeper.py`)
- Graphical interface for AI demonstration
- Automatic game with adjustable speed
- Game statistics (number of games played/won)
- Automatic restart when auto-play is enabled

### 🎲 Human Game (`minesweeper.py `)
is a classic minesweeper game for humans
- Graphical interface on tkinter

## 🎮 Management in AI Demo

### Control buttons:
- **"Auto Play"** - starts/stops the AI automatic game
- **"One move"** - The AI makes one move
- **"New Game"** - starts a new game and resets stats

### Settings:
- **Speed (ms)** - delay between AI moves (500ms by default)

### Features:
- ✅ **Automatic restart** - When auto-play is enabled, the game automatically restarts after winning/losing
- 📊 **Statistics** - shows the number of games played and wins
- ***Endless game** - The AI can play continuously until you stop

## 🧠 Technical Details

### Game status:
- `-3` - closed cell
- `-1` - mine (visible only when hit)
- `0` - empty cell
- `1-8` - the number of mines around

### DQN Architecture:
- Input layer: 16x16 (field state)
- Hidden layers: fully connected layers
- Output layer: 256 actions (16x16 cells)

### Hyperparameters of learning:
- Episodes: 10,000
- Saving the model: every 500 episodes
- Epsilon-greedy: starts at 1.0, decreases to 0.01

## 📊 Results

After training, the agent must show:
- Winning percentage: 60-80% (depends on the quality of training)
- Average number of moves to win
- Ability to avoid obvious mines

## 🔧 Requirements

- Python 3.7+
- PyTorch
- NumPy
- tkinter (usually included in Python)

## 📝 Usage examples

### Learning from scratch:
``python
python train_dqn.py
``

### Continuing education:
```python
# The model will load automatically from dqn_weights.pth
python train_dqn.py
``

### Demonstration of AI:
```python
python run_ai_game.py
```

### Human game:
`python
python minesweeper.py
``

## 🎯 Possible improvements

1. **Architecture improvement** - adding convolutional layers
2. **Other algorithms** - PPO, A3C, SAC
3. **Different field sizes** - Training in fields of different sizes
4. **Visualization of learning** - progress charts
5. **Multithreading** - parallel learning

## 🤝 Contribution to the project

Welcome:
- Bug fixes
- Algorithm improvements
- New features
- Documentation

## 📄 License

This project was created for educational purposes.

---

** Have a good game! 🎮✨**
# 🎮 DQN Minesweeper AI

Проект по обучению искусственного интеллекта играть в классическую игру "Сапер" с использованием Deep Q-Network (DQN).

## 📋 Описание проекта

Этот проект демонстрирует применение глубокого обучения с подкреплением (Reinforcement Learning) для создания ИИ-агента, способного играть в сапер. Агент обучается с помощью алгоритма Deep Q-Network и может играть на поле 16x16 с 40 минами.

## 🏗️ Архитектура проекта

```
DQN and Minesweeper Game/
├── ai_minesweeper.py      # GUI для демонстрации обученного ИИ
├── minesweeper_env.py     # RL-среда для обучения агента
├── train_dqn.py          # Скрипт обучения DQN агента
├── run_ai_game.py        # Запуск демонстрации ИИ
├── minesweeper.py        # Классическая игра для человека
├── dqn_agent.py          # Реализация DQN агента
├── requirements.txt      # Зависимости проекта
└── README.md            # Документация
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Обучение агента

```bash
python train_dqn.py
```

Обучение займет некоторое время. Модель будет сохраняться в файл `dqn_weights.pth` каждые 500 эпизодов.

### 3. Запуск демонстрации ИИ

```bash
python run_ai_game.py
```

Или напрямую:

```bash
python ai_minesweeper.py
```

## 🎯 Основные компоненты

### 🤖 DQN Agent (`dqn_agent.py`)
- Реализация Deep Q-Network агента
- Использует PyTorch для нейронной сети
- Поддерживает сохранение/загрузку обученных моделей

### 🎮 RL Environment (`minesweeper_env.py`)
- Совместимая с Gym среда для обучения
- Состояние: матрица 16x16 (закрытые/открытые клетки, числа)
- Действия: координаты клетки для открытия
- Награды: +10 за победу, -10 за поражение, +0.1 за каждую открытую клетку

### 🖥️ AI Demo (`ai_minesweeper.py`)
- Графический интерфейс для демонстрации ИИ
- Автоматическая игра с настраиваемой скоростью
- Статистика игр (количество сыгранных/выигранных)
- Автоматический перезапуск при включенной автоигре

### 🎲 Human Game (`minesweeper.py`)
- Классическая игра сапер для человека
- Графический интерфейс на tkinter

## 🎮 Управление в AI Demo

### Кнопки управления:
- **"Автоигра"** - запускает/останавливает автоматическую игру ИИ
- **"Один ход"** - ИИ делает один ход
- **"Новая игра"** - начинает новую игру и сбрасывает статистику

### Настройки:
- **Скорость (мс)** - задержка между ходами ИИ (по умолчанию 500мс)

### Особенности:
- ✅ **Автоматический перезапуск** - при включенной автоигре игра автоматически перезапускается после победы/поражения
- 📊 **Статистика** - отображается количество сыгранных игр и побед
- 🎯 **Бесконечная игра** - ИИ может играть непрерывно, пока не остановите

## 🧠 Технические детали

### Состояние игры:
- `-3` - закрытая клетка
- `-1` - мина (видна только при поражении)
- `0` - пустая клетка
- `1-8` - количество мин вокруг

### Архитектура DQN:
- Входной слой: 16x16 (состояние поля)
- Скрытые слои: полносвязные слои
- Выходной слой: 256 действий (16x16 клеток)

### Гиперпараметры обучения:
- Эпизоды: 10,000
- Сохранение модели: каждые 500 эпизодов
- Epsilon-greedy: начинается с 1.0, уменьшается до 0.01

## 📊 Результаты

После обучения агент должен показывать:
- Процент побед: 60-80% (зависит от качества обучения)
- Среднее количество ходов до победы
- Способность избегать очевидных мин

## 🔧 Требования

- Python 3.7+
- PyTorch
- NumPy
- tkinter (обычно включен в Python)

## 📝 Примеры использования

### Обучение с нуля:
```python
python train_dqn.py
```

### Продолжение обучения:
```python
# Модель автоматически загрузится из dqn_weights.pth
python train_dqn.py
```

### Демонстрация ИИ:
```python
python run_ai_game.py
```

### Игра человеком:
```python
python minesweeper.py
```

## 🎯 Возможные улучшения

1. **Улучшение архитектуры** - добавление сверточных слоев
2. **Другие алгоритмы** - PPO, A3C, SAC
3. **Разные размеры поля** - обучение на полях разного размера
4. **Визуализация обучения** - графики прогресса
5. **Многопоточность** - параллельное обучение

## 🤝 Вклад в проект

Приветствуются:
- Исправления багов
- Улучшения алгоритмов
- Новые функции
- Документация

## 📄 Лицензия

Этот проект создан в образовательных целях.

---

**Удачной игры! 🎮✨** 
