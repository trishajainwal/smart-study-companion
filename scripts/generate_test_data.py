import random
from datetime import datetime, timedelta
from src.database import insert_session

subjects = ["Python", "German", "Java Basics", "Machine Learning"]

def pick_subject(mood, focus):
    """
    Rules based on what you said:
    - Python: mood mid (3) & focus mid (3)
    - German: mood low (1-2) & focus low (1-2)
    - Java Basics: good mood (4-5) & good focus (4-5)
    - ML: mood mid (3) & focus >=4
    """

    # German
    if mood <= 2 and focus <= 2:
        return "German"

    # Python
    if mood == 3 and focus == 3:
        return "Python"

    # Machine Learning
    if mood == 3 and focus >= 4:
        return "Machine Learning"

    # Java Basics
    if mood >= 4 and focus >= 4:
        return "Java Basics"

    # fallback random
    return random.choice(subjects)

def generate_sessions(n=40):
    base_date = datetime.today() - timedelta(days=40)

    for i in range(n):
        day = base_date + timedelta(days=i)

        mood = random.randint(1, 5)
        focus = random.randint(1, 5)
        subject = pick_subject(mood, focus)

        session = {
            "date": day.strftime("%Y-%m-%d"),
            "subject": subject,
            "topic": subject + " basics",
            "duration_minutes": random.randint(20, 120),
            "perceived_difficulty": random.randint(1, 5),
            "focus_level": focus,
            "mood": mood,
            "set_goal": f"Study {subject}",
            "goal_completed": random.choice([0, 1])
        }

        insert_session(session)

    print(f">> Inserted {n} fake sessions successfully!")


if __name__ == "__main__":
    generate_sessions(40)
