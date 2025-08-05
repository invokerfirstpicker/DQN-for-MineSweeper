from gc import disable
from itertools import count
from operator import index
import tkinter as tk
from random import shuffle
import time 
class MyButton(tk.Button):
    def __init__(self, master,number, x, y, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='TimesNewRoman 15 bold',*args,**kwargs)
        self. x = x
        self. y = y
        self.number = number
        self.is_mine = False
    def __repr__(self):
        return f'B{self.number, self.is_mine}'

class Minesweeper:
    window = tk.Tk()
    buttons = []
    ROW = 16
    COLUMN = 16
    MINE = 40
    def __init__(self):
        self.buttons = []
        self.first_click = True  # Флаг первого клика
        count = 1
        for i in range(Minesweeper.ROW):
            temp = []
            for j in range(Minesweeper.COLUMN):
                btn = MyButton(Minesweeper.window, x=i, y=j, number=count)
                btn.config(command=lambda b=btn: self.click(b))
                temp.append(btn)
                count += 1
            self.buttons.append(temp)
    def createe_widget(self):
        
        for i in range(Minesweeper.ROW):
            for j in range(Minesweeper.COLUMN):
                btn = self.buttons[i][j]
                btn.grid(row=i,column=j)
    @staticmethod
    def get_mine_places():
        index = list(range(1, Minesweeper.COLUMN * Minesweeper.ROW +1))
        shuffle(index)
        return index[:Minesweeper.MINE]
    def insert_mine(self, safe_coords=None):
        # safe_coords - список координат, где не должно быть мин
        all_indexes = [
            (i, j)
            for i in range(Minesweeper.ROW)
            for j in range(Minesweeper.COLUMN)
            if not safe_coords or (i, j) not in safe_coords
        ]
        shuffle(all_indexes)
        mine_coords = all_indexes[:Minesweeper.MINE]
        for i, j in mine_coords:
            self.buttons[i][j].is_mine = True
    def count_mines_around(self, btn: MyButton):
        count_mine =0
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx ==0 and dy ==0:
                    continue
                x, y = btn.x +dx, btn.y +dy
                if 0<= x < Minesweeper.ROW and 0<= y <Minesweeper.COLUMN:
                    neighbor = self.buttons[x][y]
                    if neighbor.is_mine:
                        count_mine+=1
        return count_mine
    def click(self, clicked_button: MyButton):
        if self.first_click:
            # Определяем координаты безопасной зоны (кнопка + соседи)
            safe_coords = [
                (clicked_button.x + dx, clicked_button.y + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if 0 <= clicked_button.x + dx < Minesweeper.ROW and 0 <= clicked_button.y + dy < Minesweeper.COLUMN
            ]
            self.insert_mine(safe_coords)
            self.first_click = False
            # Открываем сразу все пустые клетки вокруг
            self.open_empty_cells(clicked_button)
            clicked_button.config(state='disabled')
            return
        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            self.LOSE()
        else:
            mines_around = self.count_mines_around(clicked_button)
            clicked_button.config(text=mines_around)
            if mines_around == 0:
                self.open_empty_cells(clicked_button)
        clicked_button.config(state='disabled')
    def show_lose_message_and_restart(self):
        lose_label = tk.Label(Minesweeper.window, text='YOU LOSE')
        lose_label.place(relx=0.5,rely=0.5, anchor="center")
        Minesweeper.window.update()
     
    def LOSE(self):
        self.show_lose_message_and_restart()
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        Minesweeper.window.after(1500, lambda:self.start())

    def open_empty_cells(self, btn: MyButton):
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = btn.x +dx, btn.y + dy
                if 0<= x < Minesweeper.ROW and 0<= y < Minesweeper.COLUMN:
                    neighbor = self.buttons[x][y]
                    if neighbor['state'] == 'disabled':
                        continue
                    mines_around = self.count_mines_around(neighbor)
                    neighbor.config(text=mines_around, state='disabled')
                    if mines_around==0:
                        self.open_empty_cells(neighbor)
    def start(self):    
        self.__init__()
        self.createe_widget()
        # Не размещаем мины заранее, только после первого клика
        Minesweeper.window.mainloop()

game = Minesweeper()
game.start()