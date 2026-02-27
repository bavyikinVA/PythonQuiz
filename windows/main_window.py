import customtkinter as ctk
from tkinter import messagebox
from windows.registration_window import RegistrationWindow
from windows.quiz_window import QuizWindow
from models.user import User


class MainWindow:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("Python Quiz — Главное меню")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        ctk.set_appearance_mode("light")        # "dark" 
        ctk.set_default_color_theme("blue")     

        self.current_user: User | None = None

        self._build_ui()
        self._center_window()

    def _center_window(self):
        self.root.update_idletasks()
        w, h = 800, 600
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # Фон-контейнер
        self.app_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.app_frame.pack(fill="both", expand=True)

        # Заголовок
        header = ctk.CTkFrame(self.app_frame, corner_radius=18, fg_color="#2c3e50")
        header.pack(fill="x", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Викторина по Python и информатике",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
        )
        title.pack(padx=20, pady=18)

        # Основной блок
        main = ctk.CTkFrame(self.app_frame, corner_radius=18)
        main.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Карточка пользователя
        self.user_frame = ctk.CTkFrame(main, corner_radius=16, fg_color="#eef5ff")
        self.user_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.user_label = ctk.CTkLabel(
            self.user_frame,
            text="Пользователь не зарегистрирован",
            text_color="#2c3e50",
            font=ctk.CTkFont(family="Arial", size=14, weight="normal"),
            justify="left",
        )
        self.user_label.pack(anchor="w", padx=18, pady=16)

        # Блок кнопок
        buttons = ctk.CTkFrame(main, fg_color="transparent")
        buttons.pack(expand=True)

        self.register_btn = ctk.CTkButton(
            buttons,
            text="Регистрация",
            command=self.open_registration,
            width=280,
            height=48,
            corner_radius=14,
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
        )
        self.register_btn.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            buttons,
            text="Начать тест",
            command=self.start_quiz,
            width=280,
            height=48,
            corner_radius=14,
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            state="disabled",
        )
        self.start_btn.pack(pady=10)

        self.exit_btn = ctk.CTkButton(
            buttons,
            text="Выход",
            command=self.root.quit,
            width=280,
            height=48,
            corner_radius=14,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
        )
        self.exit_btn.pack(pady=10)

        footer = ctk.CTkLabel(
            main,
            text="Подсказка: сначала зарегистрируйтесь, затем запускайте тест.",
            text_color="#6b7280",
            font=ctk.CTkFont(family="Arial", size=12),
        )
        footer.pack(pady=(0, 20))

    def open_registration(self):
        RegistrationWindow(self.root, self.on_registration_success)

    def on_registration_success(self, user_data: dict):
        self.current_user = User.from_dict(user_data)

        self.user_label.configure(
            text=(
                f"Привет, {self.current_user.full_name}!\n"
                f"Класс: {self.current_user.grade} • Возраст: {self.current_user.age}"
            )
        )

        self.start_btn.configure(state="normal")
        self.register_btn.configure(state="disabled")

        messagebox.showinfo(
            "Успешная регистрация",
            f"Добро пожаловать, {self.current_user.first_name}!"
        )

    def start_quiz(self):
        if not self.current_user:
            messagebox.showwarning("Внимание", "Сначала зарегистрируйтесь!")
            return

        # Скрываем главное окно
        self.root.withdraw()

        quiz_window = ctk.CTkToplevel(self.root)
        quiz_window.title(f"Тестирование — {self.current_user.full_name}")
        quiz_window.geometry("900x700")
        quiz_window.minsize(900, 700)

        def on_quiz_close():
            try:
                quiz_window.destroy()
            finally:
                self.root.deiconify()

        # При закрытии крестиком
        quiz_window.protocol("WM_DELETE_WINDOW", quiz_window.quit)

        # Окно теста
        QuizWindow(quiz_window, self.current_user, on_close=on_quiz_close)