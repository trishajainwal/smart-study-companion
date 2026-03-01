import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify 
import joblib
import pandas as pd 
from datetime import datetime
from src.database import insert_session, get_all_sessions, get_all_subjects, insert_subject, get_connection
# from src.visualize import subject_distribution, mood_focus_trend


# Paths
ML_DIR = os.path.join(os.path.dirname(__file__), "src", "ml")
MODEL_PATH = os.path.join(ML_DIR, "recommender.pkl")
ENC_PATH = os.path.join(ML_DIR, "label_encoder.pkl")

# Load trained model + label encoder
model_bundle = joblib.load(MODEL_PATH)
model = model_bundle["model"]
feature_order = model_bundle["feature_order"]
le = joblib.load(ENC_PATH)


ML_SUPPORTED_SUBJECTS = ["Python", "ML", "German", "Java Basics"]
app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/log-session", methods=["GET", "POST"])
def log_session():
    if request.method == "POST":
        date = request.form.get("date")  # get date from form
        session_data = {
            "date": date,
            "subject": request.form["subject"],
            "topic": request.form["topic"],
            "duration_minutes": int(request.form["duration"]),
            "perceived_difficulty": int(request.form["perceived_difficulty"]),
            "focus_level": int(request.form["focus_level"]),
            "mood": int(request.form["mood"]),
            "set_goal": request.form.get("set_goal", ""),
            "goal_completed": int(request.form["goal_completed"])
        }
        # Insert into database
        insert_session(session_data)
        return redirect(url_for("home"))
    subjects = get_all_subjects()
    return render_template("log_session.html", subjects=subjects)

@app.route("/logs")
def view_logs():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM study_sessions
        ORDER BY date DESC, id DESC
    """)

    logs = cursor.fetchall()
    conn.close()

    return render_template("logs.html", logs=logs)

@app.route("/suggest-subject", methods=["POST"])
def suggest_subject():
    mood = int(request.form.get("mood", 3))
    focus = int(request.form.get("focus", 3))

    row = pd.DataFrame([{
        "mood": mood,
        "focus_level": focus,
        "perceived_difficulty": 3,
        "hour": 12,
        "weekday": 2,
        "duration_minutes": 30
    }])[feature_order]

    pred_enc = model.predict(row)[0]
    subject = le.inverse_transform([pred_enc])[0]

    # CLEAN predicted subject
    subject = subject.strip()

    db_subjects = get_all_subjects()

    # Clean DB subjects too
    db_subjects_clean = [s.strip() for s in db_subjects]

    if subject not in db_subjects_clean:
        return jsonify({
            "subject": None,
            "reason": "Recommended subject not in your managed list."
        })

    reason = f"Based on your mood ({mood}) and focus ({focus})"
    return jsonify({"subject": subject, "reason": reason})

@app.route("/add-subject", methods=["POST"])
def add_subject():
    subject_name = request.form.get("subject_name")

    if subject_name:
        insert_subject(subject_name.strip())

    return redirect(url_for("log_session"))

@app.route("/subjects", methods=["GET", "POST"])
def manage_subjects():
    if request.method == "POST":
        subject_name = request.form.get("subject_name")

        if subject_name:
            insert_subject(subject_name.strip())

        return redirect(url_for("manage_subjects"))

    subjects = get_all_subjects()

    return render_template(
        "subjects.html",
        subjects=subjects,
        ml_supported=ML_SUPPORTED_SUBJECTS
    )

if __name__ == "__main__":
    app.run(debug=True)
