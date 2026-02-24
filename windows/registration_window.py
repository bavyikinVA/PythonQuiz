import tkinter as tk
from tkinter import messagebox
from base.database import register_user


class RegistrationWindow:
    def __init__(self, parent=None, on_success=None):
        self.register_btn = None
        self.entries = None
        self.parent = parent
        self.on_success = on_success

        self.window = tk.Toplevel(parent)
        self.window.title("Регистрация - QuizApp")
        self.window.geometry("600x600")
        self.window.configure(bg='white')
        self.window.resizable(False, False)

        # Делаем окно модальным
        self.window.transient(parent)
        self.window.grab_set()

        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'600x600+{x}+{y}')

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.window,
            text="Викторина по Python",
            font=("Arial", 20, "bold"),
            bg="#4a6fa5",
            fg='white',
            width=40,
            pady=15
        )
        title_label.pack()

        subtitle_label = tk.Label(
            self.window,
            text="Регистрация",
            font=("Arial", 18, "bold"),
            bg="white",
            fg='#2c3e50',
            pady=10
        )
        subtitle_label.pack()

        # Фрейм для формы
        form_frame = tk.Frame(self.window, bg="white")
        form_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)

        # Поля ввода
        fields = [
            ("Имя:", "entry_name"),
            ("Фамилия:", "entry_surname"),
            ("Класс (например, 9А):", "entry_class"),
            ("Возраст:", "entry_age")
        ]

        self.entries = {}

        for i, (label_text, entry_name) in enumerate(fields):
            # Метка
            label = tk.Label(
                form_frame,
                text=label_text,
                font=("Arial", 12),
                bg="white",
                fg='#34495e',
                anchor="w"
            )
            label.grid(row=i * 2, column=0, sticky="w", pady=(15, 5), padx=10)

            # Поле ввода
            entry = tk.Entry(
                form_frame,
                font=("Arial", 12),
                width=30,
                bg='#ecf0f1',
                relief=tk.FLAT
            )
            entry.grid(row=i * 2 + 1, column=0, sticky="ew", padx=10, pady=(0, 10))

            self.entries[entry_name] = entry

        # Настройка веса строк
        for i in range(len(fields) * 2):
            form_frame.rowconfigure(i, weight=1)

        form_frame.columnconfigure(0, weight=1)

        # Кнопка регистрации
        self.register_btn = tk.Button(
            self.window,
            text="Зарегистрироваться и начать",
            font=("Arial", 14, "bold"),
            command=self.register_user,
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=12,
            cursor="hand2"
        )
        self.register_btn.pack(pady=20)

    def register_user(self):
        """Регистрация пользователя"""
        # Получаем данные из полей
        first_name = self.entries['entry_name'].get().strip()
        last_name = self.entries['entry_surname'].get().strip()
        grade = self.entries['entry_class'].get().strip()
        age_str = self.entries['entry_age'].get().strip()

        # Валидация
        if not all([first_name, last_name, grade, age_str]):
            messagebox.showwarning("Внимание", "Заполните все поля!")
            return

        try:
            if len(grade) == 2:
                if grade[0] not in "789":
                    messagebox.showwarning("Внимание", "Введите корректный класс!")
                    return
                if grade[1] not in "АБВГД":
                    messagebox.showwarning("Внимание", "Введите корректный класс")
                    return
            elif len(grade) == 3:
                if grade[0] not in "1":
                     messagebox.showwarning("Внимание", "Введите корректный класс!")
                     return
                if grade[1] not in "01":
                    messagebox.showwarning("Внимание", "Введите корректный класс!")
                    return
                if grade[2] not in "АБВГД":
                     messagebox.showwarning("Внимание", "Введите корректный класс!")
                     return
            else:
                messagebox.showwarning("Внимание", "Введите коректный класс")
                return
            
        except ValueError:
            messagebox.showwarning("Ошибка", "Произошла ошибка при проверке класса!")

        try:
            age = int(age_str)
            if age < 14 or age > 19:
                messagebox.showwarning("Внимание", "Введите возраст от 7 до 18 лет!")
                return
        except ValueError:
            messagebox.showwarning("Внимание", "Возраст должен быть числом!")
            return

        # Регистрация в базе данных
        try:
            user_id = register_user(first_name, last_name, age, grade)

            if user_id:
                user_data = {
                    'id': user_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'grade': grade
                }

                # Вызываем callback
                if self.on_success:
                    self.on_success(user_data)

                # Закрываем окно
                self.window.destroy()
                messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            else:
                messagebox.showerror("Ошибка", "Ошибка при регистрации")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")