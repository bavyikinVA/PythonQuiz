import time
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from base.database import get_questions, save_answer, start_test_session, end_test_session


class QuizWindow:
    def __init__(self, root, user, on_close=None):
        self.root = root
        self.user = user
        self.on_close = on_close

        self.root.title(f"Тестирование — {user.full_name}")
        self.root.geometry("900x700")
        self.root.configure(fg_color="#f3f4f6")

        # Данные теста
        self.questions: list[dict] = []
        self.current_question_index = 0
        self.score = 0

        # Радио: -1 = не выбрано
        self.selected_answer = tk.IntVar(value=-1)

        self.session_id = None
        self.start_time = None
        self.session_time = None

        self._load_questions()
        self._start_session()

        self._build_ui()
        self._center_window()
        self._show_question()

    def _center_window(self):
        self.root.update_idletasks()
        w, h = 900, 700
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _load_questions(self):
        difficulty = 1
        self.questions = get_questions(difficulty=difficulty) or []

    def _start_session(self):
        self.session_time = time.time()
        self.session_id = start_test_session(self.user.id)

    def _build_ui(self):
        outer = ctk.CTkFrame(self.root, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        # Верхняя панель
        top = ctk.CTkFrame(outer, corner_radius=18, fg_color="#111827")
        top.pack(fill="x", pady=(0, 14))

        self.user_info = ctk.CTkLabel(
            top,
            text=f"Ученик: {self.user.full_name} • Класс: {self.user.grade}",
            text_color="white",
            font=ctk.CTkFont(family="Arial", size=13),
        )
        self.user_info.pack(side="left", padx=18, pady=14)

        self.counter_label = ctk.CTkLabel(
            top,
            text="",
            text_color="#f59e0b",
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
        )
        self.counter_label.pack(side="right", padx=18, pady=14)

        # Основная карточка
        main = ctk.CTkFrame(outer, corner_radius=18)
        main.pack(fill="both", expand=True)

        self.question_label = ctk.CTkLabel(
            main,
            text="",
            text_color="#111827",
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            wraplength=820,
            justify="left",
        )
        self.question_label.pack(anchor="w", padx=20, pady=(20, 10))

        self.options_frame = ctk.CTkFrame(main, fg_color="transparent")
        self.options_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Нижняя панель: прогресс + кнопка Далее
        bottom = ctk.CTkFrame(outer, corner_radius=18, fg_color="transparent")
        bottom.pack(fill="x", pady=(14, 0))

        # Прогресс
        prog_card = ctk.CTkFrame(bottom, corner_radius=16)
        prog_card.pack(side="left", fill="x", expand=True)

        self.score_label = ctk.CTkLabel(
            prog_card,
            text="",
            text_color="#065f46",
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
        )
        self.score_label.pack(anchor="w", padx=16, pady=(12, 4))

        self.progress = ctk.CTkProgressBar(prog_card, height=16, corner_radius=10)
        self.progress.set(0.0)
        self.progress.pack(fill="x", padx=16, pady=(0, 12))

        # Кнопка Далее
        self.next_btn = ctk.CTkButton(
            bottom,
            text="Далее →",
            command=self._next_question,
            width=180,
            height=48,
            corner_radius=14,
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
        )
        self.next_btn.pack(side="right", padx=(14, 0))

    def _update_progress(self):
        total = max(len(self.questions), 1)
        progress_value = (self.current_question_index + 1) / total
        self.progress.set(progress_value)
        self.score_label.configure(text=f"Счет: {self.score}/{len(self.questions)}")

    def _show_question(self):
        # Если вопросов нет — сразу корректно завершаем
        if not self.questions:
            self._show_empty_state()
            return

        if self.current_question_index >= len(self.questions):
            self._complete_test()
            return

        # очистка старых вариантов
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        question = self.questions[self.current_question_index]

        self.counter_label.configure(
            text=f"Вопрос {self.current_question_index + 1}/{len(self.questions)}"
        )
        self.question_label.configure(text=question["text"])

        self.start_time = time.time()
        self.selected_answer.set(-1) 

        # варианты
        for i, option in enumerate(question["options"]):
            rb = ctk.CTkRadioButton(
                self.options_frame,
                text=option,
                variable=self.selected_answer,
                value=i + 1,
                font=ctk.CTkFont(family="Arial", size=14),
            )
            rb.pack(fill="x", pady=8, padx=10)

        self._update_progress()

    def _save_current_answer(self):
        chosen = self.selected_answer.get()
        if chosen == -1:
            return

        question = self.questions[self.current_question_index]
        correct = (chosen == question["answers"])

        if correct:
            self.score += 1
            self._update_progress()

        save_answer(
            self.user.id,
            question["id"],
            correct,
            round(time.time() - self.start_time, 2),
        )

    def _next_question(self):
        if self.selected_answer.get() == -1:
            messagebox.showwarning("Внимание", "Выберите ответ перед продолжением!")
            return

        self._save_current_answer()
        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self._show_question()
        else:
            self._complete_test()

    def _complete_test(self):
        end_session_time = round(time.time() - self.session_time)
        result_percent = end_test_session(self.session_id, self.score, end_session_time)
        self._show_results(result_percent)

    def _show_results(self, result_percent: float):
        for widget in self.root.winfo_children():
            widget.destroy()

        outer = ctk.CTkFrame(self.root, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        card = ctk.CTkFrame(outer, corner_radius=18)
        card.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            card,
            text="Тестирование завершено!",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color="#111827",
        )
        title.pack(pady=(30, 10))

        result_text = (
            f"Правильных ответов: {self.score} из {len(self.questions)}\n"
            f"Процент выполнения: {result_percent}%"
        )
        result_label = ctk.CTkLabel(
            card,
            text=result_text,
            font=ctk.CTkFont(family="Arial", size=18),
            text_color="#374151",
            justify="center",
        )
        result_label.pack(pady=(10, 20))

        # оценка
        if result_percent >= 90:
            grade_text, grade_color = "Отлично!", "#16a34a"
        elif result_percent >= 75:
            grade_text, grade_color = "Хорошо!", "#f59e0b"
        elif result_percent >= 50:
            grade_text, grade_color = "Удовлетворительно", "#f97316"
        else:
            grade_text, grade_color = "Нужно повторить материал", "#ef4444"

        grade = ctk.CTkLabel(
            card,
            text=grade_text,
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color=grade_color,
        )
        grade.pack(pady=(0, 26))

        btn = ctk.CTkButton(
            card,
            text="Выйти из программы",
            width=240,
            height=50,
            corner_radius=14,
            fg_color="#ef4444",
            hover_color="#dc2626",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            command=self._exit_application,
        )
        btn.pack(pady=(0, 30))

    def _show_empty_state(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        outer = ctk.CTkFrame(self.root, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        card = ctk.CTkFrame(outer, corner_radius=18)
        card.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            card,
            text="В базе нет вопросов",
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
            text_color="#111827",
        )
        title.pack(pady=(40, 10))

        text = ctk.CTkLabel(
            card,
            text="Добавьте вопросы в quiz.db и запустите тест снова.",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#6b7280",
        )
        text.pack(pady=(0, 20))

        btn = ctk.CTkButton(
            card,
            text="Закрыть",
            width=200,
            height=48,
            corner_radius=14,
            command=self._close,
        )
        btn.pack(pady=(0, 40))

    def _close(self):
        if callable(self.on_close):
            self.on_close()
        else:
            try:
                self.root.destroy()
            except Exception:
                pass

    def _exit_application(self):
        self.root.quit()
        self.root.destroy()