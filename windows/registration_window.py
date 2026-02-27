import customtkinter as ctk
from tkinter import messagebox

from base.database import register_user


class RegistrationWindow:
    def __init__(self, parent=None, on_success=None):
        self.parent = parent
        self.on_success = on_success
        self.entries: dict[str, ctk.CTkEntry] = {}

        self.window = ctk.CTkToplevel(parent)
        self.window.title("Регистрация — QuizApp")
        self.window.geometry("600x600")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self._center_window()
        self._build_ui()

    def _center_window(self):
        self.window.update_idletasks()
        w, h = 600, 600
        x = (self.window.winfo_screenwidth() // 2) - (w // 2)
        y = (self.window.winfo_screenheight() // 2) - (h // 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        root = ctk.CTkFrame(self.window, fg_color="transparent")
        root.pack(fill="both", expand=True)

        header = ctk.CTkFrame(root, corner_radius=18, fg_color="#2c3e50")
        header.pack(fill="x", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="Викторина по Python",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
        )
        title.pack(padx=20, pady=18)

        card = ctk.CTkFrame(root, corner_radius=18)
        card.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        subtitle = ctk.CTkLabel(
            card,
            text="Регистрация",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
        )
        subtitle.pack(anchor="w", padx=20, pady=(20, 10))

        form = ctk.CTkFrame(card, corner_radius=16, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        fields = [
            ("Имя", "entry_name", "Введите имя"),
            ("Фамилия", "entry_surname", "Введите фамилию"),
            ("Класс (например, 9А)", "entry_class", "Например: 9А"),
            ("Возраст", "entry_age", "Например: 15"),
        ]

        for label_text, key, placeholder in fields:
            lbl = ctk.CTkLabel(
                form,
                text=label_text,
                text_color="#374151",
                font=ctk.CTkFont(family="Arial", size=13, weight="normal"),
            )
            lbl.pack(anchor="w", pady=(12, 6))

            entry = ctk.CTkEntry(
                form,
                placeholder_text=placeholder,
                height=40,
                corner_radius=12,
            )
            entry.pack(fill="x")
            self.entries[key] = entry

        self.register_btn = ctk.CTkButton(
            card,
            text="Зарегистрироваться и начать",
            command=self.register_user,
            height=48,
            corner_radius=14,
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
        )
        self.register_btn.pack(padx=20, pady=(10, 18), fill="x")

        hint = ctk.CTkLabel(
            card,
            text="Класс допускается: 7–11 и буквы АБВГД (пример: 9А, 10Б).",
            text_color="#6b7280",
            font=ctk.CTkFont(family="Arial", size=12),
            wraplength=520,
            justify="left",
        )
        hint.pack(anchor="w", padx=20, pady=(0, 18))

        # Enter = регистрация
        self.window.bind("<Return>", lambda _: self.register_user())

    def register_user(self):
        first_name = self.entries["entry_name"].get().strip()
        last_name = self.entries["entry_surname"].get().strip()
        grade = self.entries["entry_class"].get().strip().upper()
        age_str = self.entries["entry_age"].get().strip()

        if not all([first_name, last_name, grade, age_str]):
            messagebox.showwarning("Внимание", "Заполните все поля!")
            return

        # валидация класса (7–11 + буква АБВГД)
        if len(grade) == 2:
            if grade[0] not in "789":
                messagebox.showwarning("Внимание", "Введите корректный класс (7–11)!")
                return
            if grade[1] not in "АБВГД":
                messagebox.showwarning("Внимание", "Введите корректную букву класса (АБВГД)!")
                return
        elif len(grade) == 3:
            if grade[0] != "1" or grade[1] not in "01":
                messagebox.showwarning("Внимание", "Введите корректный класс (10 или 11)!")
                return
            if grade[2] not in "АБВГД":
                messagebox.showwarning("Внимание", "Введите корректную букву класса (АБВГД)!")
                return
        else:
            messagebox.showwarning("Внимание", "Введите корректный класс (например 9А или 10Б).")
            return

        # Валидация возраста
        try:
            age = int(age_str)
            if age < 14 or age > 19:
                messagebox.showwarning("Внимание", "Введите возраст от 14 до 19 лет!")
                return
        except ValueError:
            messagebox.showwarning("Внимание", "Возраст должен быть числом!")
            return

        try:
            user_id = register_user(first_name, last_name, age, grade)
            if not user_id:
                messagebox.showerror("Ошибка", "Ошибка при регистрации.")
                return

            user_data = {
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "age": age,
                "grade": grade,
            }

            if self.on_success:
                self.on_success(user_data)

            self.window.destroy()
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")