import tkinter as tk

from database import get_questions
from windows.main_window import MainWindow


def main():
    root = tk.Tk() # создание главного окна
    MainWindow(root)
    root.mainloop() # запуск приложения

if __name__ == '__main__':
    main()