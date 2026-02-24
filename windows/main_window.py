import tkinter as tk
from tkinter import messagebox
from windows.registration_window import RegistrationWindow
from windows.quiz_window import QuizWindow
from models.user import User

    
class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz - Главное меню")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f8ff')

        self.current_user = None
        self.create_widgets()

        # Центрируем окно
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'800x600+{x}+{y}')

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Викторина по Python и информатике",
            font=("Arial", 24, "bold"),
            bg='#4a6fa5',
            fg='white',
            pady=20
        )
        title_label.pack(fill=tk.X)

        # Контейнер для основного содержимого
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)

        # Информация о пользователе
        self.user_frame = tk.Frame(main_frame, bg='#e6f2ff', relief=tk.RIDGE, bd=2)
        self.user_frame.pack(fill=tk.X, pady=(0, 30))

        self.user_label = tk.Label(
            self.user_frame,
            text="Пользователь не зарегистрирован",
            font=("Arial", 14),
            bg='#e6f2ff',
            fg='#666',
            pady=10
        )
        self.user_label.pack()

        # Кнопки
        button_frame = tk.Frame(main_frame, bg='#f0f8ff')
        button_frame.pack(expand=True)

        # Кнопка регистрации
        self.register_btn = tk.Button(
            button_frame,
            text="Регистрация",
            font=("Arial", 16, "bold"),
            command=self.open_registration,
            bg='#2ecc71',
            fg='white',
            width=20,
            height=2,
            cursor="hand2"
        )
        self.register_btn.pack(pady=10)

        # Кнопка начала теста
        self.start_btn = tk.Button(
            button_frame,
            text="Начать тест",
            font=("Arial", 16, "bold"),
            command=self.start_quiz,
            bg='#3498db',
            fg='white',
            width=20,
            height=2,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.start_btn.pack(pady=10)


        # Кнопка выхода
        self.exit_btn = tk.Button(
            button_frame,
            text="Выход",
            font=("Arial", 16, "bold"),
            command=self.root.quit,
            bg='#e74c3c',
            fg='white',
            width=20,
            height=2,
            cursor="hand2"
        )
        self.exit_btn.pack(pady=10)

    def open_registration(self):
        """Открытие окна регистрации"""
        RegistrationWindow(self.root, self.on_registration_success)

    def on_registration_success(self, user_data):
        """Обработка успешной регистрации"""
        self.current_user = User.from_dict(user_data)

        # Обновляем информацию о пользователе
        self.user_label.config(
            text=f"Привет, {self.current_user.full_name}!\n"
                 f"Класс: {self.current_user.grade}, Возраст: {self.current_user.age}",
            fg='#2c3e50'
        )

        # активируем кнопку старта теста
        self.start_btn.config(state=tk.NORMAL)
        # блокируем кнопку регистрации
        self.register_btn.config(state=tk.DISABLED)

        messagebox.showinfo(
            "Успешная регистрация",
            f"Добро пожаловать, {self.current_user.first_name}!"
        )

    def start_quiz(self):
        """Запуск тестирования"""
        if self.current_user:
            # Скрываем главное окно
            self.root.withdraw()

            # Создаем окно тестирования
            quiz_window = tk.Toplevel(self.root)
            QuizWindow(quiz_window, self.current_user)

            # Обработка закрытия окна теста
            quiz_window.protocol("WM_DELETE_WINDOW",
                                 lambda: self.on_quiz_close(quiz_window))
        else:
            messagebox.showwarning("Внимание", "Сначала зарегистрируйтесь!")

    def on_quiz_close(self, quiz_window):
        """Обработка закрытия окна теста"""
        quiz_window.destroy()
        self.root.deiconify()  # Показываем главное окно