📚 SMART STUDY COMPANION

A Flask-based web app that recommends what subject to study based on your current mood and focus level.
It uses a trained machine learning model to make suggestions instead of random selection.

OVERVIEW

This project combines machine learning and web development to solve a simple problem: deciding what to study at a given moment.

*Users input their mood and focus level, and the system predicts a suitable subject.

FEATURES

1. Add and manage subjects

2. Log study sessions

3. ML-based subject recommendation

4. Validation to prevent unknown subject predictions

5. Clean modal-based UI

6. SQLite database integration

HOW IT WORKS

The model was trained using:
Mood ,Focus level, Perceived difficulty, Hour of day, Weekday, Study duration

The predicted subject is verified against the user’s managed subjects before being displayed.

TECH STACK

Python, Flask, scikit-learn, Pandas, SQLite, HTML, CSS

