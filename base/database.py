import sqlite3
from datetime import datetime


def create_database():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    # таблица студентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL)
    ''')

    # Таблица вопросов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text_questions TEXT NOT NULL,
        options TEXT NOT NULL, 
        answers INTEGER, 
        difficulty_level INTEGER DEFAULT 1)
    ''')

    # Таблица результатов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        score INTEGER DEFAULT 0,
        score_percent REAL DEFAULT 0.0,
        test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        time_spent INTEGER DEFAULT 0, 
        FOREIGN KEY (student_id) REFERENCES students (id))
    ''')

    # таблица ответов на вопросы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   student_id INTEGER NOT NULL,
                   question_id INTEGER NOT NULL,
                   is_correct INTEGER DEFAULT 0,
                   time_spent INTEGER DEFAULT 0,
                   FOREIGN KEY (student_id) REFERENCES students (id),
                   FOREIGN KEY (question_id) REFERENCES questions (id))
    ''')

    conn.commit()
    conn.close()


def add_questions(questions: list):
    """ Добавление вопросов в базу данных """
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    for q in questions:
        # преобразуем ответы в строку
        answers_str = ','.join(str(a) for a in q['answers'])
        options_str = ','.join(q['options'])
        
        cursor.execute('''
        INSERT INTO questions (text_questions, options, answers, difficulty_level)
        VALUES (?, ?, ?, ?)
        ''', (
            q['text'],
            options_str,
            answers_str,
            q.get('difficulty', 1)  # Значение по умолчанию 1, если не указана сложность
        ))

    conn.commit()
    conn.close()


def register_user(first_name, last_name, age, grade):
    """Регистрация нового пользователя"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO students (first_name, last_name, age, grade)
    VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, age, grade))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return user_id


def get_questions(difficulty=None):
    """Получение вопросов из базы данных"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    if difficulty:
        cursor.execute('''
        SELECT id, text_questions, options, answers, difficulty_level 
        FROM questions 
        WHERE difficulty_level = ?''', (difficulty,))
    else:
        cursor.execute('''
        SELECT id, text_questions, options, answers, difficulty_level 
        FROM questions''')

    questions = []
    for row in cursor.fetchall():
        q_id, text, options_str, answers_str, difficulty = row
        options = options_str.split(',')
        answers = int(answers_str)

        questions.append({
            'id': q_id,
            'text': text,
            'options': options,
            'answers': answers,
            'difficulty': difficulty
        })

    conn.close()
    return questions


def save_answer(student_id, question_id, is_correct, time_spent):
    """Сохранение ответа пользователя с замером времени"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO answers (student_id, question_id, is_correct, time_spent)
    VALUES (?, ?, ?, ?)
    ''', (student_id, question_id, 1 if is_correct else 0, time_spent))

    conn.commit()
    conn.close()


def start_test_session(student_id):
    """Начало новой сессии тестирования"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO results (student_id, score, score_percent, test_date, time_spent)
    VALUES (?, 0, 0.0, ?, 0)
    ''', (student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    result_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return result_id

def end_test_session(result_id, correct_answers, total_time_spent):
    """Завершение сессии тестирования"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    # Получаем общее количество вопросов
    cursor.execute('SELECT COUNT(*) FROM questions')
    total_questions = cursor.fetchone()[0]
    
    # Вычисляем процент
    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    cursor.execute('''
    UPDATE results
    SET score = ?, 
        score_percent = ?,
        time_spent = ?
    WHERE id = ?
    ''', (
        correct_answers,
        round(score_percentage, 2),
        total_time_spent,
        result_id))

    conn.commit()
    conn.close()

    return round(score_percentage, 2)


def get_user_stats(user_id):
    """Получение статистики пользователя"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT COUNT(*) as results,
           AVG(score_percentage) as avg_score,
           MAX(score_percentage) as best_score
    FROM test_sessions 
    WHERE user_id = ?
    ''', (user_id,))

    stats = cursor.fetchone()
    conn.close()

    return {
        'total_tests': stats[0] if stats[0] else 0,
        'avg_score': round(stats[1], 2) if stats[1] else 0,
        'best_score': round(stats[2], 2) if stats[2] else 0
    }


# инициализация базы данных при импорте
create_database()