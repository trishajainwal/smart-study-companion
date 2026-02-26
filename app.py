from flask import Flask, render_template, request, redirect, url_for, jsonify 
from datetime import datetime
from src.database import (
    insert_session,
    get_all_sessions,
    get_connection,
    get_all_subjects,
    insert_subject,
    create_subjects_table
)
from src.visualize import subject_distribution, weekly_stacked_data, mood_focus_trend
from src.recommender import recommend_subject
import joblib
import os
from flask import Flask, request, jsonify
import pandas as pd 

app = Flask(__name__)

# Paths
ML_DIR = os.path.join(os.path.dirname(__file__), "src", "ml")
MODEL_PATH = os.path.join(ML_DIR, "recommender.pkl")
ENC_PATH = os.path.join(ML_DIR, "label_encoder.pkl")

# Load trained model + label encoder
model_bundle = joblib.load(MODEL_PATH)
model = model_bundle["model"]
feature_order = model_bundle["feature_order"]
le = joblib.load(ENC_PATH)
print("Feature order:", feature_order)
print("Model classes:", le.classes_)

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

@app.route('/weekly-overview')
def weekly_overview():
    return render_template("weekly_overview.html")

@app.route('/weekly-data')
def weekly_data():
    import pandas as pd
    df = get_all_sessions()

    if df.empty:
        return {"dates": [], "stackedDatasets": [], "mood": [], "focus": [], "subjects": [], "subjectDurations": [], "subjectColors": []}

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df = df.sort_values('date')

    # Unique sorted dates
    dates = sorted(df['date'].dt.strftime('%d %b').unique(), key=lambda d: datetime.strptime(d, '%d %b'))

    subjects = sorted(df['subject'].unique())
    stackedDatasets = []
    topic_dict = {subject: [[] for _ in range(len(dates))] for subject in subjects}
    dataset_dict = {subject: [0]*len(dates) for subject in subjects}
    date_index = {date: i for i, date in enumerate(dates)}

    # Single loop over rows
    for _, row in df.iterrows():
        day_str = row['date'].strftime('%d %b')
        idx = date_index[day_str]
        dataset_dict[row['subject']][idx] += row['duration_minutes']
        topic_dict[row['subject']][idx].append(row['topic'])

    pastel_colors = ["#FFDAB9", "#FFB6C1", "#B0E0E6", "#AFEEEE", "#E6E6FA", "#F5DEB3"]

    for i, subject in enumerate(subjects):
        stackedDatasets.append({
            "label": subject,
            "data": dataset_dict[subject],
            "backgroundColor": pastel_colors[i % len(pastel_colors)],
            "topics": topic_dict[subject]
        })

    # Mood & Focus aligned with dates
    mood = [df[df['date'].dt.strftime('%d %b') == d]['mood'].mean().round(1) for d in dates]
    focus = [df[df['date'].dt.strftime('%d %b') == d]['focus_level'].mean().round(1) for d in dates]

    # Subject distribution
    subj_dist = df.groupby('subject')['duration_minutes'].sum()
    subjectDurations = subj_dist.tolist()
    subjectColors = [pastel_colors[i % len(pastel_colors)] for i in range(len(subj_dist))]

    return {
        "dates": dates,
        "stackedDatasets": stackedDatasets,
        "mood": mood,
        "focus": focus,
        "subjects": list(subj_dist.index),
        "subjectDurations": subjectDurations,
        "subjectColors": subjectColors
    }

@app.route('/weekly-stacked-data')
def weekly_stacked():
    return jsonify(weekly_stacked_data())

@app.route('/mood-focus-data')
def mood_focus():
    return jsonify(mood_focus_trend())

@app.route('/subject-distribution')
def subject_dist():
    return jsonify(subject_distribution())

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
