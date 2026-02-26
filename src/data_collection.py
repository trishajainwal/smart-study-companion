def collect_study_session():
    session = {
        "date": input("Date (YYYY-MM-DD): "),
        "subject": input("Subject: "),
        "topic": input("Topic: "),
        "duration_minutes": int(input("Duration (minutes): ")),
        "perceived_difficulty": int(input("Difficulty (1-5): ")),
        "focus_level": int(input("Focus level (1-5): ")),
        "mood": int(input("Mood (1-5): ")),
        "set_goal": input("Goal for this session: "),
        "goal_completed": int(input("Goal completed? (0 = No, 1 = Yes): "))
    }
    return session

if __name__ == "__main__":
    print(collect_study_session())
