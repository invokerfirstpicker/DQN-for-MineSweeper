import numpy as np
import random

class MinesweeperEnv:
    """
    Простая RL-среда для сапёра (16x16, 40 мин), совместимая с Gym.
    Состояние: матрица 16x16 (0 - закрыто, -1 - мина, 1-8 - число мин вокруг, -2 - открытое пустое)
    Действие: (x, y) - координаты клетки, которую открыть
    """
    def __init__(self, rows=16, cols=16, n_mines=40):
        self.rows = rows
        self.cols = cols
        self.n_mines = n_mines
        self.action_space = rows * cols
        self.observation_space = (rows, cols)
        self.reset()

    def reset(self):
        # 0 - закрыто, -1 - мина, -2 - открытое пустое, 1-8 - число мин вокруг
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.visible = np.zeros((self.rows, self.cols), dtype=int)  # 0 - закрыто, 1 - открыто
        self.mines = set()
        self.done = False
        self.first_move = True
        self.opened = 0
        return self._get_obs()

    def _place_mines(self, safe_coords):
        # safe_coords - список координат, где не должно быть мин (первый клик и соседи)
        all_cells = [(i, j) for i in range(self.rows) for j in range(self.cols) if (i, j) not in safe_coords]
        mines = random.sample(all_cells, self.n_mines)
        for (i, j) in mines:
            self.board[i, j] = -1
            self.mines.add((i, j))
        # Заполняем числа вокруг мин
        for (i, j) in mines:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < self.rows and 0 <= nj < self.cols and self.board[ni, nj] != -1:
                        self.board[ni, nj] += 1

    def step(self, action):
        """
        action: int (от 0 до rows*cols-1) или (x, y)
        Возвращает: obs, reward, done, info
        """
        if isinstance(action, int):
            x, y = divmod(action, self.cols)
        else:
            x, y = action
        if self.done or self.visible[x, y]:
            return self._get_obs(), 0.0, self.done, {}
        # Первый ход - размещаем мины
        if self.first_move:
            safe = [(x + dx, y + dy) for dx in [-1,0,1] for dy in [-1,0,1]
                    if 0 <= x+dx < self.rows and 0 <= y+dy < self.cols]
            self._place_mines(safe)
            self.first_move = False
        # Если мина - проигрыш
        if self.board[x, y] == -1:
            self.visible[x, y] = 1
            self.done = True
            reward = -10.0
            return self._get_obs(), reward, self.done, {"lose": True}
        # Открываем клетку (и пустые вокруг)
        opened_now = self._open_cell(x, y)
        self.opened += opened_now
        # Проверка на победу
        if self.opened == self.rows * self.cols - self.n_mines:
            self.done = True
            return self._get_obs(), 10.0, True, {"win": True}
        return self._get_obs(), 0.1 * opened_now, False, {}

    def _open_cell(self, x, y):
        # BFS для открытия пустых клеток
        stack = [(x, y)]
        opened = 0
        while stack:
            i, j = stack.pop()
            if self.visible[i, j]:
                continue
            self.visible[i, j] = 1
            opened += 1
            if self.board[i, j] == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < self.rows and 0 <= nj < self.cols and not self.visible[ni, nj]:
                            stack.append((ni, nj))
        return opened

    def _get_obs(self):
        # Возвращает видимое поле: -3 (закрыто), -1 (мину не показываем), 0-8 (открыто)
        obs = np.full((self.rows, self.cols), -3, dtype=int)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.visible[i, j]:
                    obs[i, j] = self.board[i, j]
        return obs.copy()

    def render(self):
        # Текстовый вывод поля
        for i in range(self.rows):
            row = ''
            for j in range(self.cols):
                if self.visible[i, j]:
                    if self.board[i, j] == -1:
                        row += '* '
                    else:
                        row += f'{self.board[i, j]} '
                else:
                    row += '# '
            print(row)
        print()

if __name__ == "__main__":
    env = MinesweeperEnv()
    obs = env.reset()
    env.render()
    done = False
    while not done:
        # Случайный ход
        action = random.randint(0, env.action_space - 1)
        obs, reward, done, info = env.step(action)
        env.render()
        print(f"Reward: {reward}")
        if 'win' in info:
            print('WIN!')
        if 'lose' in info:
            print('LOSE!')
