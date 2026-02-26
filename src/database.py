import sqlite3
import os
import pandas as pd

# Always resolve project root correctly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "study_sessions.db")

def get_connection():
    """Return a SQLite connection to the study sessions database."""
    return sqlite3.connect(DB_PATH)

def create_table():
    """Create the study_sessions table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            subject TEXT,
            topic TEXT,
            duration_minutes INTEGER,
            perceived_difficulty INTEGER, 
            focus_level INTEGER,
            mood INTEGER,
            set_goal TEXT,
            goal_completed INTEGER
        )
    """)

    conn.commit()
    conn.close()

def insert_session(session_dict):
    """Insert a study session into the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_sessions (
            date, subject, topic, duration_minutes, perceived_difficulty, 
            focus_level, mood, set_goal, goal_completed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_dict["date"],
        session_dict["subject"],
        session_dict["topic"],
        session_dict["duration_minutes"],
        session_dict["perceived_difficulty"],
        session_dict["focus_level"],
        session_dict["mood"],
        session_dict["set_goal"],
        session_dict["goal_completed"]
    ))

    conn.commit()
    conn.close()

def get_all_sessions():
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM study_sessions", conn)
    finally:
        conn.close()
    return df

def create_subjects_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM subjects ORDER BY name ASC")
    subjects = [row[0] for row in cursor.fetchall()]

    conn.close()
    return subjects


def insert_subject(name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # ignore duplicates

    conn.close()

if __name__ == "__main__":
    create_table()
    create_subjects_table()
    print("Database initialized with default subjects.")
