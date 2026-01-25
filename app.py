import tkinter as tk
from gui_registration import RegistrationWindow
from main import PythonQuizApp

class QuizApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Скрываем главное окно пока что
        self.user_data = None
        
        # Запускаем окно регистрации
        self.show_registration()
        
    def show_registration(self):
        """Показываем окно регистрации"""
        registration_window = RegistrationWindow(
            parent=self.root,
            on_success=self.on_registration_success
        )
        
    def on_registration_success(self, user_data):
        """Обратный вызов при успешной регистрации"""
        self.user_data = user_data
        print(f"Пользователь зарегистрирован: {user_data}")
        
        # Запускаем основную викторину
        self.start_quiz()
    
    def start_quiz(self):
        """Запускаем основную викторину"""
        # Создаем новое окно для викторины
        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("Викторина по основам Python")
        quiz_window.geometry("600x500")
        
        # Передаем user_data в викторину (можно использовать для статистики)
        app = PythonQuizApp(quiz_window, user_data=self.user_data)
        
        # Обработка закрытия окна викторины
        quiz_window.protocol("WM_DELETE_WINDOW", self.on_quiz_close)
    
    def on_quiz_close(self):
        """Обработка закрытия приложения"""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Запуск главного цикла"""
        self.root.mainloop()

if __name__ == "__main__":
    app = QuizApplication()
    app.run()