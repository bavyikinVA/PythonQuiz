import sqlite3
from datetime import datetime


def create_database():
    """Создание базы данных и таблиц"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL,
    )
    ''')

    # Таблица вопросов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text_question TEXT NOT NULL,
        options TEXT NOT NULL, 
        answers TEXT NOT NULL, 
        difficulty_level INTEGER DEFAULT 1,
        category TEXT DEFAULT 'Python'
    )
    ''')

    # Таблица результатов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        user_answer TEXT,
        is_correct INTEGER DEFAULT 0, 
        answer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
    ''')

    conn.commit()
    conn.close()


def add_sample_questions():
    """Добавление примерных вопросов в базу данных"""
    questions = [
        {
            'text': 'Что выведет print(type(5))?',
            'options': ['int', 'str', 'float', 'bool'],
            'answers': '0',
            'difficulty': 1,
            'category': 'Python'
        },
        {
            'text': 'Какой оператор используется для возведения в степень?',
            'options': ['^', '**', 'pow()', '//'],
            'answers': '1',
            'difficulty': 1,
            'category': 'Python'
        },
        {
            'text': 'Что такое список (list) в Python?',
            'options': [
                'Изменяемая последовательность',
                'Неизменяемая последовательность',
                'Словарь',
                'Множество'
            ],
            'answers': '0',
            'difficulty': 2,
            'category': 'Python'
        }
    ]

    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    for q in questions:
        cursor.execute('''
        INSERT INTO questions (text_question, options, answers, difficulty_level, category)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            q['text'],
            ','.join(q['options']),
            q['answers'],
            q['difficulty'],
            q['category']
        ))

    conn.commit()
    conn.close()


def register_user(first_name, last_name, age, grade):
    """Регистрация нового пользователя"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (first_name, last_name, age, grade)
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
        SELECT id, text_question, options, answers, difficulty_level 
        FROM questions 
        WHERE difficulty_level = ?
        LIMIT ?
        ''', (difficulty, limit))
    else:
        cursor.execute('''
        SELECT id, text_question, options, answers, difficulty_level 
        FROM questions 
        LIMIT ?
        ''', (limit,))

    questions = []
    for row in cursor.fetchall():
        q_id, text, options_str, answers_str, difficulty = row
        options = options_str.split(',')
        answers = [int(a) for a in answers_str.split(',')]

        questions.append({
            'id': q_id,
            'text': text,
            'options': options,
            'answers': answers,
            'difficulty': difficulty
        })

    conn.close()
    return questions


def save_answer(user_id, question_id, user_answer, is_correct):
    """Сохранение ответа пользователя"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO results (user_id, question_id, user_answer, is_correct)
    VALUES (?, ?, ?, ?)
    ''', (user_id, question_id, str(user_answer), 1 if is_correct else 0))

    conn.commit()
    conn.close()


def start_test_session(user_id):
    """Начало новой сессии тестирования"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO test_sessions (user_id, start_time)
    VALUES (?, ?)
    ''', (user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return session_id


def end_test_session(session_id, total_questions, correct_answers):
    """Завершение сессии тестирования"""
    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE test_sessions 
    SET end_time = ?, 
        total_questions = ?, 
        correct_answers = ?, 
        score_percentage = ?
    WHERE id = ?
    ''', (
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total_questions,
        correct_answers,
        round(score_percentage, 2),
        session_id
    ))

    conn.commit()
    conn.close()

    return score_percentage


def get_user_stats(user_id):
    """Получение статистики пользователя"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT COUNT(*) as total_tests,
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


# Инициализация базы данных при импорте
create_database()