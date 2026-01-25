import tkinter as tk
from tkinter import messagebox
from database import registration
import sqlite3

class RegistrationWindow:
    def __init__(self, parent=None, on_success=None):
        self.parent = parent
        self.on_success = on_success  # Callback функция при успешной регистрации
        
        self.window = tk.Toplevel(parent)
        self.window.title("Регистрация - QuizApp")
        self.window.geometry("600x600")
        self.window.configure(bg='white')
        self.window.resizable(False, False)
        
        # Делаем окно модальным
        self.window.transient(parent)
        self.window.grab_set()
        
        # Центрируем окно
        self.center_window()
        
        self.create_widgets()
        
        # Обработка закрытия окна
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def center_window(self):
        """Центрирует окно на экране"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{600}x{600}+{x}+{y}')
    
    def create_widgets(self):
        """Создание виджетов окна регистрации"""
        # Заголовок
        title_label = tk.Label(
            self.window, 
            text="Викторина по основам Python", 
            font=("Arial", 16, "bold"), 
            bg="#71ddcb",
            fg='#333',
            width=40,
            pady=10
        )
        title_label.pack(pady=20)
        
        registration_label = tk.Label(
            self.window, 
            text="Регистрация", 
            font=("Arial", 16, "bold"), 
            bg="#71ddcb",
            fg='#333',
            width=20,
            pady=5
        )
        registration_label.pack(pady=15)
        
        # Фрейм для полей ввода
        form_frame = tk.Frame(self.window, bg="white")
        form_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Имя
        label_name = tk.Label(
            form_frame, 
            text="Имя:", 
            font=("Arial", 12),  
            bg="white",
            fg='#333'
        )
        label_name.grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        self.entry_name = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.entry_name.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
        
        # Фамилия
        label_surname = tk.Label(
            form_frame, 
            text="Фамилия:", 
            font=("Arial", 12),  
            bg="white",
            fg='#333'
        )
        label_surname.grid(row=1, column=0, sticky="w", pady=10, padx=10)
        
        self.entry_surname = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.entry_surname.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
        
        # Класс
        label_class = tk.Label(
            form_frame, 
            text="Класс:", 
            font=("Arial", 12),  
            bg="white",
            fg='#333'
        )
        label_class.grid(row=2, column=0, sticky="w", pady=10, padx=10)
        
        self.entry_class = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.entry_class.grid(row=2, column=1, pady=10, padx=10, sticky="ew")
        
        # Возраст
        label_age = tk.Label(
            form_frame, 
            text="Возраст:", 
            font=("Arial", 12),  
            bg="white",
            fg='#333'
        )
        label_age.grid(row=3, column=0, sticky="w", pady=10, padx=10)
        
        self.entry_age = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.entry_age.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
        
        # Настройка веса колонок
        form_frame.columnconfigure(1, weight=1)
        
        # Фрейм для кнопки
        button_frame = tk.Frame(self.window, bg="white")
        button_frame.pack(pady=30)
        
        # Кнопка "Начать"
        self.btn_start =tk.Button(
            button_frame,
            text="Начать викторину",
            font=("Arial", 12, "bold"),
            command=self.start_quiz,
            bg="#4CAF50",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.btn_start.pack()
        
        # Подсказка
        hint_label = tk.Label(
            self.window,
            text="Заполните все поля для начала викторины",
            font=("Arial", 10),
            bg="white",
            fg="#666"
        )
        hint_label.pack(pady=10)
    
    def start_quiz(self):
        """Функция, которая вызывается при нажатии кнопки 'Начать викторину'"""
        first_name = self.entry_name.get().strip()
        last_name = self.entry_surname.get().strip()
        grade = self.entry_class.get().strip()
        age = self.entry_age.get().strip()
        
        # Проверка, что все поля заполнены
        if not all([first_name, last_name, grade, age]):
            messagebox.showwarning("Внимание", "Заполните все поля!")
            return
        
        # Проверка возраста
        try:
            age_int = int(age)
            if age_int < 5 or age_int > 100:
                messagebox.showwarning("Внимание", "Введите корректный возраст!")
                return
        except ValueError:
            messagebox.showwarning("Внимание", "Возраст должен быть числом!")
            return
        
        # Регистрация пользователя
        try:
            user_id = registration(first_name, last_name, age_int, grade)
            
            if user_id is not None:
                # Создаем словарь с данными пользователя
                user_data = {
                    'id': user_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age_int,
                    'grade': grade,
                    'full_name': f"{first_name} {last_name}"
                }
                
                # Вызываем callback с данными пользователя
                if self.on_success:
                    self.on_success(user_data)
                
                # Закрываем окно регистрации
                self.window.destroy()
                
            else:
                messagebox.showerror("Ошибка", "Не удалось зарегистрировать пользователя!")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при регистрации: {str(e)}")
    
    def on_close(self):
        """Обработка закрытия окна регистрации"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.parent.quit()
            self.parent.destroy()

# Функция для запуска только окна регистрации (для тестирования)
def main():
    root = tk.Tk()
    root.withdraw()
    app = RegistrationWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()