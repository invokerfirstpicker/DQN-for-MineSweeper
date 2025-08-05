import tkinter as tk
from random import shuffle
import time
import numpy as np
from dqn_agent import DQNAgent
import os

class MyButton(tk.Button):
    def __init__(self, master, number, x, y, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='TimesNewRoman 15 bold',*args,**kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
    def __repr__(self):
        return f'B{self.number, self.is_mine}'

class AIMinesweeper:
    def __init__(self, agent_path='dqn_weights.pth'):
        self.window = tk.Tk()
        self.window.title("AI Minesweeper - DQN Agent")
        self.buttons = []
        self.ROW = 16
        self.COLUMN = 16
        self.MINE = 40
        
        # Инициализация агента
        self.agent = None
        self.agent_path = agent_path
        self.load_agent()
        
        # Переменные игры
        self.first_click = True
        self.game_done = False
        self.auto_play = False
        self.delay = 500  # миллисекунды между ходами
        
        # Статистика игр
        self.games_played = 0
        self.games_won = 0
        
        # Создание интерфейса
        self.create_interface()
        self.create_buttons()
        
    def load_agent(self):
        """Загружает обученного агента"""
        try:
            if os.path.exists(self.agent_path):
                print('Загружаю обученного агента...')
                self.agent = DQNAgent((self.ROW, self.COLUMN), self.ROW * self.COLUMN)
                self.agent.load(self.agent_path)
                self.agent.epsilon = 0.0  # Отключаем случайность для демонстрации
                print('Агент загружен успешно!')
                print(f'Размер состояния: {self.ROW}x{self.COLUMN}')
                print(f'Количество действий: {self.ROW * self.COLUMN}')
            else:
                print(f'Файл модели {self.agent_path} не найден!')
                self.agent = None
        except Exception as e:
            print(f'Ошибка загрузки агента: {e}')
            import traceback
            traceback.print_exc()
            self.agent = None
    
    def create_interface(self):
        """Создает элементы управления"""
        # Панель управления
        control_frame = tk.Frame(self.window)
        control_frame.pack(pady=10)
        
        # Кнопки управления
        self.auto_play_btn = tk.Button(control_frame, text="Автоигра", command=self.toggle_auto_play)
        self.auto_play_btn.pack(side=tk.LEFT, padx=5)
        
        self.step_btn = tk.Button(control_frame, text="Один ход", command=self.make_ai_step)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(control_frame, text="Новая игра", command=self.reset_game)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Настройка скорости
        speed_frame = tk.Frame(control_frame)
        speed_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(speed_frame, text="Скорость (мс):").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="500")
        speed_entry = tk.Entry(speed_frame, textvariable=self.speed_var, width=5)
        speed_entry.pack(side=tk.LEFT, padx=5)
        
        # Информация
        self.info_label = tk.Label(control_frame, text="Готов к игре", font=('Arial', 12))
        self.info_label.pack(side=tk.RIGHT, padx=10)
        
        # Создаем отдельный фрейм для игрового поля
        self.game_frame = tk.Frame(self.window)
        self.game_frame.pack(pady=10)
        
    def create_buttons(self):
        """Создает игровое поле"""
        self.buttons = []
        count = 1
        for i in range(self.ROW):
            temp = []
            for j in range(self.COLUMN):
                btn = MyButton(self.game_frame, x=i, y=j, number=count)
                btn.config(command=lambda b=btn: self.click(b))
                temp.append(btn)
                count += 1
            self.buttons.append(temp)
        
        # Размещаем кнопки
        for i in range(self.ROW):
            for j in range(self.COLUMN):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)
    
    def toggle_auto_play(self):
        """Включает/выключает автоматическую игру"""
        if not self.agent:
            self.info_label.config(text="Агент не загружен!")
            print("Агент не загружен!")
            return
            
        self.auto_play = not self.auto_play
        if self.auto_play:
            self.auto_play_btn.config(text="Остановить")
            self.info_label.config(text="Автоигра запущена")
            print("Автоигра запущена!")
            self.make_ai_step()
        else:
            self.auto_play_btn.config(text="Автоигра")
            self.info_label.config(text="Автоигра остановлена")
            print("Автоигра остановлена!")
    
    def make_ai_step(self):
        """Делает один ход агента"""
        if not self.agent or self.game_done:
            print("Агент не загружен или игра закончена")
            return
            
        # Получаем текущее состояние
        state = self.get_current_state()
        state_input = state.astype(np.float32) / 8.0
        
        # Выбираем действие
        action = self.agent.select_action(state_input)
        x, y = divmod(action, self.COLUMN)
        
        print(f"Агент выбирает ход: ({x}, {y})")
        
        # Проверяем, что клетка еще не открыта
        if self.buttons[x][y]['state'] == 'disabled':
            print(f"Клетка ({x}, {y}) уже открыта, выбираем другую...")
            # Ищем закрытую клетку
            for i in range(self.ROW):
                for j in range(self.COLUMN):
                    if self.buttons[i][j]['state'] != 'disabled':
                        x, y = i, j
                        print(f"Выбираем случайную закрытую клетку: ({x}, {y})")
                        break
                else:
                    continue
                break
        
        # Выполняем ход
        self.click(self.buttons[x][y])
        
        # Если автоигра включена и игра не закончена, планируем следующий ход
        if self.auto_play and not self.game_done:
            try:
                delay = int(self.speed_var.get())
            except:
                delay = 500
            self.window.after(delay, self.make_ai_step)
    
    def get_current_state(self):
        """Получает текущее состояние игры для агента"""
        state = np.full((self.ROW, self.COLUMN), -3, dtype=int)
        for i in range(self.ROW):
            for j in range(self.COLUMN):
                btn = self.buttons[i][j]
                if btn['state'] == 'disabled':
                    # Если кнопка открыта, берем текст (количество мин вокруг)
                    if btn.cget('text') == '*':
                        state[i][j] = -1  # мина
                    else:
                        try:
                            state[i][j] = int(btn.cget('text'))
                        except ValueError:
                            state[i][j] = 0  # пустая клетка
                else:
                    state[i][j] = -3  # закрыто
        return state
    
    def get_mine_places(self):
        """Генерирует позиции мин"""
        index = list(range(1, self.COLUMN * self.ROW + 1))
        shuffle(index)
        return index[:self.MINE]
    
    def insert_mine(self, safe_coords=None):
        """Размещает мины на поле"""
        all_indexes = [
            (i, j)
            for i in range(self.ROW)
            for j in range(self.COLUMN)
            if not safe_coords or (i, j) not in safe_coords
        ]
        shuffle(all_indexes)
        mine_coords = all_indexes[:self.MINE]
        for i, j in mine_coords:
            self.buttons[i][j].is_mine = True
    
    def count_mines_around(self, btn: MyButton):
        """Подсчитывает количество мин вокруг кнопки"""
        count_mine = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = btn.x + dx, btn.y + dy
                if 0 <= x < self.ROW and 0 <= y < self.COLUMN:
                    neighbor = self.buttons[x][y]
                    if neighbor.is_mine:
                        count_mine += 1
        return count_mine
    
    def click(self, clicked_button: MyButton):
        """Обрабатывает клик по кнопке"""
        if self.game_done:
            return
            
        if self.first_click:
            # Определяем координаты безопасной зоны
            safe_coords = [
                (clicked_button.x + dx, clicked_button.y + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if 0 <= clicked_button.x + dx < self.ROW and 0 <= clicked_button.y + dy < self.COLUMN
            ]
            self.insert_mine(safe_coords)
            self.first_click = False
            self.open_empty_cells(clicked_button)
            clicked_button.config(state='disabled')
            return
            
        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            self.game_over(False)
        else:
            mines_around = self.count_mines_around(clicked_button)
            clicked_button.config(text=mines_around)
            if mines_around == 0:
                self.open_empty_cells(clicked_button)
        clicked_button.config(state='disabled')
        
        # Проверка на победу
        self.check_win()
    
    def open_empty_cells(self, btn: MyButton):
        """Открывает пустые клетки вокруг"""
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = btn.x + dx, btn.y + dy
                if 0 <= x < self.ROW and 0 <= y < self.COLUMN:
                    neighbor = self.buttons[x][y]
                    if neighbor['state'] == 'disabled':
                        continue
                    mines_around = self.count_mines_around(neighbor)
                    neighbor.config(text=mines_around, state='disabled')
                    if mines_around == 0:
                        self.open_empty_cells(neighbor)
    
    def check_win(self):
        """Проверяет, выиграл ли игрок"""
        opened_count = 0
        for row in self.buttons:
            for btn in row:
                if btn['state'] == 'disabled' and not btn.is_mine:
                    opened_count += 1
        
        if opened_count == self.ROW * self.COLUMN - self.MINE:
            self.game_over(True)
    
    def game_over(self, won):
        """Обрабатывает окончание игры"""
        self.game_done = True
        
        # Обновляем статистику
        self.games_played += 1
        if won:
            self.games_won += 1
            self.info_label.config(text=f"ПОБЕДА! 🎉 (Игр: {self.games_played}, Побед: {self.games_won})")
            # Показываем все мины зеленым
            for row in self.buttons:
                for btn in row:
                    if btn.is_mine:
                        btn.config(text="*", background='green', disabledforeground='white')
        else:
            self.info_label.config(text=f"ПОРАЖЕНИЕ! 💥 (Игр: {self.games_played}, Побед: {self.games_won})")
            # Показываем все мины красным
            for row in self.buttons:
                for btn in row:
                    if btn.is_mine:
                        btn.config(text="*", background='red', disabledforeground='white')
        
        # Если автоигра включена, перезапускаем игру через 2 секунды
        if self.auto_play:
            self.window.after(2000, self.auto_restart_game)
        else:
            self.auto_play = False
            self.auto_play_btn.config(text="Автоигра")
    
    def auto_restart_game(self):
        """Автоматически перезапускает игру при включенной автоигре"""
        if self.auto_play:
            print("Автоматический перезапуск игры...")
            self.reset_game()
            # Продолжаем автоигру
            self.make_ai_step()
    
    def reset_game(self):
        """Сбрасывает игру"""
        self.game_done = False
        self.first_click = True
        # Не отключаем автоигру при сбросе, если она была включена
        if not self.auto_play:
            self.auto_play_btn.config(text="Автоигра")
            # Сбрасываем статистику только при ручном сбросе
            self.games_played = 0
            self.games_won = 0
        self.info_label.config(text="Готов к игре")
        
        # Очищаем поле
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        
        # Создаем новое поле
        self.create_buttons()
    
    def start(self):
        """Запускает игру"""
        self.window.mainloop()

if __name__ == "__main__":
    game = AIMinesweeper()
    game.start() 