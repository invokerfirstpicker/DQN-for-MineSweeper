#!/usr/bin/env python3
"""
Скрипт для запуска AI игры в сапёр
"""

import os
import sys
from ai_minesweeper import AIMinesweeper

def main():
    print("=== AI Minesweeper - DQN Agent ===")
    print()
    
    # Проверяем наличие модели
    model_path = 'dqn_weights.pth'
    if not os.path.exists(model_path):
        print(f"❌ Файл модели {model_path} не найден!")
        print("Сначала обучите агента, запустив:")
        print("python train_dqn.py")
        print()
        input("Нажмите Enter для выхода...")
        return
    
    print(f"✅ Модель найдена: {model_path}")
    print()
    print("Управление:")
    print("- 'Автоигра' - запускает автоматическую игру агента")
    print("- 'Один ход' - агент делает один ход")
    print("- 'Новая игра' - начинает новую игру")
    print("- 'Скорость' - настройка скорости автоигры (в миллисекундах)")
    print()
    print("Запускаю игру...")
    print()
    
    try:
        game = AIMinesweeper(model_path)
        game.start()
    except Exception as e:
        print(f"❌ Ошибка запуска игры: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main() 