import pandas as pd
from src.database import insert_session

CSV_PATH = "data/test_sessions.csv"

def load_data():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()  # remove any spaces in headers

    print(f"Loading {len(df)} sessions from CSV into the database...")

    for i, row in df.iterrows():
        # Convert date string to datetime object
        date_obj = pd.to_datetime(row['date'], errors='coerce')
        if pd.isna(date_obj):
            print(f"Skipping row {i+1} due to invalid date: {row['date']}")
            continue

        session_dict = {
            "date": date_obj.strftime("%Y-%m-%d %H:%M:%S"),  # ISO format
            "subject": row['subject'],
            "topic": row['topic'],
            "duration_minutes": row['duration_minutes'],
            "perceived_difficulty": row['perceived_difficulty'],
            "focus_level": row['focus_level'],
            "mood": row['mood'],
            "set_goal": row.get('set_goal', ""),
            "goal_completed": 1 if str(row['goal_completed']).lower() in ["yes", "1", "true"] else 0
        }

        insert_session(session_dict)
        print(f"Inserted session {i+1}: {row['subject']} - {row['topic']} on {session_dict['date']}")

    print("All test data loaded successfully!")

if __name__ == "__main__":
    load_data()
