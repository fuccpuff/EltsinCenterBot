# database.py
import sqlite3
from config import DATABASE_NAME

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                interests TEXT,
                language TEXT,
                quest_progress INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                user_id INTEGER,
                command TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id, first_name, language):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        if cursor.fetchone() is None:
            cursor.execute(
                'INSERT INTO users (user_id, first_name, language) VALUES (?, ?, ?)',
                (user_id, first_name, language)
            )
            self.conn.commit()

    def get_user_language(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT language FROM users WHERE user_id=?', (user_id,))
        result = cursor.fetchone()
        return result['language'] if result else None

    def update_user_language(self, user_id, language):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE users SET language=? WHERE user_id=?',
            (language, user_id)
        )
        self.conn.commit()

    def update_user_interests(self, user_id, interests):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE users SET interests=? WHERE user_id=?',
            (interests, user_id)
        )
        self.conn.commit()

    def save_stats(self, user_id, command):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO stats (user_id, command) VALUES (?, ?)',
            (user_id, command)
        )
        self.conn.commit()

    def get_statistics(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM stats')
        total_messages = cursor.fetchone()[0]
        return {
            'total_users': total_users,
            'total_messages': total_messages
        }

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_id FROM users')
        return cursor.fetchall()