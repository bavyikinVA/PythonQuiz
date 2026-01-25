import tkinter as tk
from tkinter import messagebox
import sqlite3

class PythonQuizApp:
    def __init__(self, root):
        self.score_label = None
        self.next_button = None
        self.options_frame = None
        self.question_label = None
        self.title_label = None
        self.counter_label = None
        self.root = root
        self.root.title("Викторина по основам Python")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Данные викторины
        self.questions = self.load_questions_from_db()
        
        self.current_question = 0
        self.score = 0
        self.selected_answer = tk.IntVar(value=-1)
        
        self.create_widgets()
        self.show_question()
    
    @staticmethod
    def load_questions_from_db():
        questions = []
        con = sqlite3.connect("quiz.db")
        cursor = con.cursor()
        cursor.execute("SELECT text_questions, options, answers FROM questions")
        for row in cursor.fetchall():
            text_questions, options, answers = row
            option_list = options.split(", ")
            question_dict = {"question": text_questions, "options": option_list, "correct": answers-1}
            questions.append(question_dict)
        con.close()
        print(f"Загружено {len(questions)} из db" )
        return questions
    
    def create_widgets(self):
        # Заголовок
        self.title_label = tk.Label(
            self.root, 
            text="Викторина по основам Python", 
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#333'
        )
        self.title_label.pack(pady=20)
        
        # Счетчик вопросов
        self.counter_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#666'
        )
        self.counter_label.pack()
        
        # Вопрос
        self.question_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#333',
            wraplength=550,
            justify="center"
        )
        self.question_label.pack(pady=30)
        
        # Фрейм для вариантов ответов
        self.options_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.options_frame.pack(pady=20)
        
        # Кнопка "Далее"
        self.next_button = tk.Button(
            self.root,
            text="Следующий вопрос",
            font=("Arial", 12),
            command=self.next_question,
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.next_button.pack(pady=20)
        
        # Метка для отображения счета
        self.score_label = tk.Label(
            self.root,
            text=f"Счет: {self.score}/{len(self.questions)}",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#2196F3'
        )
        self.score_label.pack()
    
    def show_question(self):
        # Очищаем предыдущие варианты ответов
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Обновляем счетчик вопросов
        self.counter_label.config(
            text=f"Вопрос {self.current_question + 1} из {len(self.questions)}"
        )
        
        # Показываем текущий вопрос
        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data["question"])
        
        # Создаем радиокнопки для вариантов ответов
        self.selected_answer.set(-1)
        for i, option in enumerate(question_data["options"]):
            rb = tk.Radiobutton(
                self.options_frame,
                text=option,
                variable=self.selected_answer,
                value=i,
                font=("Arial", 11),
                bg='#f0f0f0',
                command=self.enable_next_button
            )
            rb.pack(anchor='w', pady=5)
        
        # Обновляем состояние кнопки
        self.next_button.config(state=tk.DISABLED)
    
    def enable_next_button(self):
        """Активирует кнопку 'Далее' когда выбран ответ"""
        self.next_button.config(state=tk.NORMAL)
    
    def next_question(self):
        """Обрабатывает переход к следующему вопросу"""
        if self.selected_answer.get() == -1:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите ответ!")
            return
        
        # Проверяем ответ
        if self.selected_answer.get() == self.questions[self.current_question]["correct"]:
            self.score += 1
            self.score_label.config(text=f"Счет: {self.score}/{len(self.questions)}")
        
        # Переходим к следующему вопросу или завершаем викторину
        self.current_question += 1
        
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_results()
    
    def show_results(self):
        """Показывает результаты викторины"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Результаты
        result_text = f"Викторина завершена!\n\nВаш результат: {self.score}/{len(self.questions)}"
        
        result_label = tk.Label(
            self.root,
            text=result_text,
            font=("Arial", 14, "bold"),
            bg='#f0f0f0',
            fg='#333',
            justify="center"
        )
        result_label.pack(expand=True, pady=50)
        
        # Оценка
        percentage = (self.score / len(self.questions)) * 100
        if percentage >= 80:
            grade = "Отлично! 🎉"
            color = "#4CAF50"
        elif percentage >= 60:
            grade = "Хорошо! 👍"
            color = "#FF9800"
        else:
            grade = "Попробуйте еще раз! 💪"
            color = "#F44336"
        
        grade_label = tk.Label(
            self.root,
            text=grade,
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg=color
        )
        grade_label.pack(pady=10)
        
        # Кнопка для перезапуска
        restart_button = tk.Button(
            self.root,
            text="Начать заново",
            font=("Arial", 12),
            command=self.restart_quiz,
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10
        )
        restart_button.pack(pady=20)
    
    def restart_quiz(self):
        """Перезапускает викторину"""
        self.current_question = 0
        self.score = 0
        self.selected_answer.set(-1)
        
        # Очищаем окно и создаем виджеты заново
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.create_widgets()
        self.show_question()

def main():
    root = tk.Tk()
    PythonQuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()