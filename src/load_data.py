import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "study_sessions.db")

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM study_sessions", conn)
    conn.close()

    # Encode categorical columns
    df['subject_code'] = df['subject'].astype('category').cat.codes
    df['topic_code'] = df['topic'].astype('category').cat.codes

    return df

if __name__ == "__main__":
    df = load_data()
    print(df.head())
