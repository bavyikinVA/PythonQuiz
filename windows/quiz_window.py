import tkinter as tk
from tkinter import messagebox
from base.database import get_questions, save_answer, start_test_session, end_test_session


class QuizWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"Тестирование - {user.full_name}")
        self.root.geometry("900x700")
        self.root.configure(bg='#ecf0f1')

        # Данные тестирования
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.selected_answer = tk.StringVar(value="")
        self.session_id = None

        # Загрузка вопросов и начало сессии
        self.load_questions()
        self.start_session()

        self.create_widgets()
        self.show_question()

        # Центрирование
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'900x700+{x}+{y}')

    def load_questions(self):
        """Загрузка вопросов из базы данных"""
        # Можно добавить логику выбора сложности на основе класса
        difficulty_map = {
            '9': 1,
            '10': 2,
            '11': 3
        }

        grade_num = self.user.grade[0] if self.user.grade and self.user.grade[0].isdigit() else '9'
        difficulty = difficulty_map.get(grade_num, 1)

        self.questions = get_questions(difficulty=difficulty)

    def start_session(self):
        """Начало сессии тестирования"""
        self.session_id = start_test_session(self.user.id)

    def create_widgets(self):
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50')
        top_frame.pack(fill=tk.X, padx=20, pady=10)

        # Информация о пользователе
        user_info = tk.Label(
            top_frame,
            text=f"Ученик: {self.user.full_name} | Класс: {self.user.grade}",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='white'
        )
        user_info.pack(side=tk.LEFT)

        # Счетчик вопросов
        self.counter_label = tk.Label(
            top_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#f39c12'
        )
        self.counter_label.pack(side=tk.RIGHT)

        # Основная область
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

        # Вопрос
        self.question_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 16),
            bg='#ecf0f1',
            fg='#2c3e50',
            wraplength=800,
            justify="left",
            anchor="w"
        )
        self.question_label.pack(pady=(20, 30), anchor="w")

        # Фрейм для вариантов ответов
        self.options_frame = tk.Frame(main_frame, bg='#ecf0f1')
        self.options_frame.pack(fill=tk.BOTH, expand=True)

        # Кнопки навигации
        nav_frame = tk.Frame(self.root, bg='#ecf0f1')
        nav_frame.pack(fill=tk.X, padx=40, pady=20)

        # Кнопка "Назад" (только если не первый вопрос)
        self.back_btn = tk.Button(
            nav_frame,
            text="← Назад",
            font=("Arial", 12),
            command=self.previous_question,
            bg='#95a5a6',
            fg='white',
            width=10,
            state=tk.DISABLED
        )
        self.back_btn.pack(side=tk.LEFT)

        # Кнопка "Далее"
        self.next_btn = tk.Button(
            nav_frame,
            text="Далее →",
            font=("Arial", 12, "bold"),
            command=self.next_question,
            bg='#3498db',
            fg='white',
            width=10
        )
        self.next_btn.pack(side=tk.RIGHT)

        # Прогресс-бар
        self.progress_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.progress_frame.pack(fill=tk.X, padx=40, pady=(0, 20))

        self.progress_label = tk.Label(
            self.progress_frame,
            text="Прогресс:",
            font=("Arial", 10),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.progress_label.pack(side=tk.LEFT)

        self.progress_bar = tk.Canvas(
            self.progress_frame,
            width=400,
            height=20,
            bg='#bdc3c7',
            highlightthickness=0
        )
        self.progress_bar.pack(side=tk.LEFT, padx=(10, 0))

        # Текущий счет
        self.score_label = tk.Label(
            self.progress_frame,
            text=f"Счет: {self.score}/{len(self.questions)}",
            font=("Arial", 12, "bold"),
            bg='#ecf0f1',
            fg='#27ae60'
        )
        self.score_label.pack(side=tk.RIGHT)

    def show_question(self):
        """Отображение текущего вопроса"""
        # Очищаем предыдущие варианты
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        if self.current_question_index >= len(self.questions):
            self.complete_test()
            return

        question = self.questions[self.current_question_index]

        # Обновляем счетчик
        self.counter_label.config(
            text=f"Вопрос {self.current_question_index + 1}/{len(self.questions)}"
        )

        # Обновляем вопрос
        self.question_label.config(text=question['text'])

        # Создаем радиокнопки для вариантов ответа
        self.selected_answer.set("")

        for i, option in enumerate(question['options']):
            rb = tk.Radiobutton(
                self.options_frame,
                text=option,
                variable=self.selected_answer,
                value=str(i),
                font=("Arial", 14),
                bg='#ecf0f1',
                fg='#2c3e50',
                anchor="w",
                padx=20,
                pady=10,
                cursor="hand2"
            )
            rb.pack(fill=tk.X, pady=5)

        # Обновляем прогресс
        self.update_progress()

        # Обновляем состояние кнопок
        self.back_btn.config(
            state=tk.NORMAL if self.current_question_index > 0 else tk.DISABLED
        )

    def update_progress(self):
        """Обновление прогресс-бара"""
        progress = (self.current_question_index + 1) / len(self.questions)

        self.progress_bar.delete("progress")
        width = 400 * progress
        self.progress_bar.create_rectangle(
            0, 0, width, 20,
            fill='#2ecc71',
            outline='',
            tags="progress"
        )

    def save_current_answer(self):
        """Сохранение текущего ответа"""
        if self.selected_answer.get():
            question = self.questions[self.current_question_index]
            user_answer = int(self.selected_answer.get())
            is_correct = user_answer == question['answers']

            if is_correct:
                self.score += 1
                self.score_label.config(text=f"Счет: {self.score}/{len(self.questions)}")

            save_answer(
                self.user.id,
                question['id'],
                user_answer,
                is_correct
            )

    def next_question(self):
        """Переход к следующему вопросу"""
        if not self.selected_answer.get():
            messagebox.showwarning("Внимание", "Выберите ответ перед продолжением!")
            return

        # Сохраняем текущий ответ
        self.save_current_answer()

        # Переход к следующему вопросу
        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            self.complete_test()

    def previous_question(self):
        """Переход к предыдущему вопросу"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def complete_test(self):
        """Завершение тестирования"""
        # Завершаем сессию
        end_test_session(
            self.session_id,
            len(self.questions),
            self.score
        )

        # Показываем результаты
        self.show_results()

    def show_results(self):
        """Показать результаты теста"""
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()

        # Результаты
        percentage = (self.score / len(self.questions)) * 100

        result_frame = tk.Frame(self.root, bg='#ecf0f1')
        result_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)

        # Заголовок
        title_label = tk.Label(
            result_frame,
            text="Тестирование завершено!",
            font=("Arial", 24, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50',
            pady=20
        )
        title_label.pack()

        # Результат
        result_text = (
            f"Правильных ответов: {self.score} из {len(self.questions)}\n\n"
            f"Процент выполнения: {percentage:.1f}%\n\n"
        )

        result_label = tk.Label(
            result_frame,
            text=result_text,
            font=("Arial", 18),
            bg='#ecf0f1',
            fg='#34495e',
            pady=30
        )
        result_label.pack()

        # Оценка
        if percentage >= 90:
            grade = "Отлично! 🏆"
            color = "#27ae60"
        elif percentage >= 75:
            grade = "Хорошо! 👍"
            color = "#f39c12"
        elif percentage >= 60:
            grade = "Удовлетворительно"
            color = "#e67e22"
        else:
            grade = "Нужно повторить материал 📚"
            color = "#e74c3c"

        grade_label = tk.Label(
            result_frame,
            text=grade,
            font=("Arial", 20, "bold"),
            bg='#ecf0f1',
            fg=color,
            pady=20
        )
        grade_label.pack()

        # Кнопки
        button_frame = tk.Frame(result_frame, bg='#ecf0f1')
        button_frame.pack(pady=40)

        # Кнопка "Пройти еще раз"
        retry_btn = tk.Button(
            button_frame,
            text="Пройти еще раз",
            font=("Arial", 14),
            command=self.retry_test,
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            cursor="hand2"
        )
        retry_btn.pack(side=tk.LEFT, padx=10)

        # Кнопка "В главное меню"
        home_btn = tk.Button(
            button_frame,
            text="В главное меню",
            font=("Arial", 14),
            command=self.root.destroy,
            bg='#2ecc71',
            fg='white',
            padx=20,
            pady=10,
            cursor="hand2"
        )
        home_btn.pack(side=tk.LEFT, padx=10)

    def retry_test(self):
        """Перезапуск теста"""
        # Сброс параметров
        self.current_question_index = 0
        self.score = 0
        self.selected_answer.set("")

        # Новая сессия
        self.session_id = start_test_session(self.user.id)

        # Перезагрузка вопросов
        self.load_questions()

        # Очистка и пересоздание виджетов
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_widgets()
        self.show_question()