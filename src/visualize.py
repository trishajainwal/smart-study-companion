# !!!WORK IN PROGRESS - VISUALIZATION MODULE UNDER REFACTORING!!!
# import pandas as pd
# from src.database import get_connection

# # Helper: load all study sessions as DataFrame
# def load_sessions():
#     conn = get_connection()
#     df = pd.read_sql("SELECT * FROM study_sessions", conn)
#     conn.close()
#     df['date'] = pd.to_datetime(df['date'], errors='coerce')
#     return df.dropna(subset=['date'])


# # Weekly Stacked Bar (Daily/Weekly Study Duration)
# def weekly_stacked_data():
#     df = load_sessions()
#     if df.empty:
#         return {"labels": [], "datasets": []}

#     # Use last 7 days
#     last_week = df['date'].max() - pd.Timedelta(days=6)
#     df = df[df['date'] >= last_week].sort_values('date')

#     # Prepare labels (dates)
#     labels = df['date'].dt.strftime('%d %b').unique().tolist()
    
#     # Subjects
#     subjects = sorted(df['subject'].unique())
#     dataset_dict = {subject: [0]*len(labels) for subject in subjects}
#     topic_dict = {subject: [[] for _ in labels] for subject in subjects}
#     label_index = {label:i for i,label in enumerate(labels)}

#     # Fill dataset values and topics
#     for _, row in df.iterrows():
#         idx = label_index[row['date'].strftime('%d %b')]
#         dataset_dict[row['subject']][idx] += row['duration_minutes']
#         topic_dict[row['subject']][idx].append(row['topic'])

#     # Pastel colors
#     pastel_colors = ["#FFDAB9", "#FFB6C1", "#B0E0E6", "#AFEEEE", "#E6E6FA", "#F5DEB3"]

#     datasets = []
#     for i, subject in enumerate(subjects):
#         datasets.append({
#             "label": subject,
#             "data": dataset_dict[subject],
#             "backgroundColor": pastel_colors[i % len(pastel_colors)],
#             "topics": topic_dict[subject]
#         })

#     return {"labels": labels, "datasets": datasets}


# # Mood & Focus Trend (Multi-line chart)
# def mood_focus_trend():
#     df = load_sessions()
#     if df.empty:
#         return {"labels": [], "datasets": [], "quote": ""}

#     last_week = df['date'].max() - pd.Timedelta(days=6)
#     df = df[df['date'] >= last_week].sort_values('date')
#     labels = df['date'].dt.strftime('%d %b').tolist()

#     mood = df['mood'].tolist()
#     focus = df['focus_level'].tolist()

#     # Personalized quote
#     if mood[-1] >= 5 and focus[-1] >= 5:
#         quote = "You’re on fire! Keep the streak alive 🔥"
#     elif mood[-1] < 5 and focus[-1] >= 5:
#         quote = "Brains working hard, don’t forget breaks 🧠💪"
#     elif mood[-1] >= 5 and focus[-1] < 5:
#         quote = "Feeling good! Let’s channel it into focus 💡"
#     else:
#         quote = "Time to recharge, you’ve got this 🌱"

#     datasets = [
#         {"label": "Mood", "data": mood, "borderColor": "#FF8C00", "fill": False, "tension":0.2},
#         {"label": "Focus", "data": focus, "borderColor": "#1E90FF", "fill": False, "tension":0.2}
#     ]

#     return {"labels": labels, "datasets": datasets, "quote": quote}


# # Subject-wise Study Distribution (Donut chart)
# def subject_distribution():
#     df = load_sessions()
#     if df.empty:
#         return {"labels": [], "datasets": []}

#     pivot = df.groupby('subject')['duration_minutes'].sum()
#     labels = pivot.index.tolist()
#     data = pivot.values.tolist()

#     pastel_colors = ["#FFDAB9", "#FFB6C1", "#B0E0E6", "#AFEEEE", "#E6E6FA", "#F5DEB3"]

#     datasets = [{"data": data, "backgroundColor": [pastel_colors[i % len(pastel_colors)] for i in range(len(labels))]}]

#     return {"labels": labels, "datasets": datasets}





"""
Weekly analytics routes — Work in Progress.
Temporarily disabled in main application.
"""

# @app.route('/weekly-overview')
# def weekly_overview():
#     return render_template("weekly_overview.html")

# @app.route('/weekly-data')
# def weekly_data():
#     import pandas as pd
#     df = get_all_sessions()

#     if df.empty:
#         return {"dates": [], "stackedDatasets": [], "mood": [], "focus": [], "subjects": [], "subjectDurations": [], "subjectColors": []}

#     df['date'] = pd.to_datetime(df['date'], errors='coerce')
#     df = df.dropna(subset=['date'])
#     df = df.sort_values('date')

#     # Unique sorted dates
#     dates = sorted(df['date'].dt.strftime('%d %b').unique(), key=lambda d: datetime.strptime(d, '%d %b'))

#     subjects = sorted(df['subject'].unique())
#     stackedDatasets = []
#     topic_dict = {subject: [[] for _ in range(len(dates))] for subject in subjects}
#     dataset_dict = {subject: [0]*len(dates) for subject in subjects}
#     date_index = {date: i for i, date in enumerate(dates)}

#     # Single loop over rows
#     for _, row in df.iterrows():
#         day_str = row['date'].strftime('%d %b')
#         idx = date_index[day_str]
#         dataset_dict[row['subject']][idx] += row['duration_minutes']
#         topic_dict[row['subject']][idx].append(row['topic'])

#     pastel_colors = ["#FFDAB9", "#FFB6C1", "#B0E0E6", "#AFEEEE", "#E6E6FA", "#F5DEB3"]

#     for i, subject in enumerate(subjects):
#         stackedDatasets.append({
#             "label": subject,
#             "data": dataset_dict[subject],
#             "backgroundColor": pastel_colors[i % len(pastel_colors)],
#             "topics": topic_dict[subject]
#         })

#     # Mood & Focus aligned with dates
#     mood = [df[df['date'].dt.strftime('%d %b') == d]['mood'].mean().round(1) for d in dates]
#     focus = [df[df['date'].dt.strftime('%d %b') == d]['focus_level'].mean().round(1) for d in dates]

#     # Subject distribution
#     subj_dist = df.groupby('subject')['duration_minutes'].sum()
#     subjectDurations = subj_dist.tolist()
#     subjectColors = [pastel_colors[i % len(pastel_colors)] for i in range(len(subj_dist))]

#     return {
#         "dates": dates,
#         "stackedDatasets": stackedDatasets,
#         "mood": mood,
#         "focus": focus,
#         "subjects": list(subj_dist.index),
#         "subjectDurations": subjectDurations,
#         "subjectColors": subjectColors
#     }

# @app.route('/weekly-stacked-data')
# def weekly_stacked():
#     return jsonify(weekly_stacked_data())

# @app.route('/mood-focus-data')
# def mood_focus():
#     return jsonify(mood_focus_trend())

# @app.route('/subject-distribution')
# def subject_dist():
#     return jsonify(subject_distribution())