import customtkinter as ctk
from windows.main_window import MainWindow

def main():
    root = ctk.CTk()
    MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()