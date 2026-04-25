"""Главный модуль для запуска Weather Diary"""
import tkinter as tk
from gui import WeatherDiaryGUI

def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = WeatherDiaryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()