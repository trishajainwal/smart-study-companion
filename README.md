📚 SMART STUDY COMPANION

A Flask-based web app that recommends what subject to study based on your current mood and focus level.
It uses a trained machine learning model to make suggestions instead of random selection.

Overview

This project combines machine learning and web development to solve a simple problem: deciding what to study at a given moment.
Users input their mood and focus level, and the system predicts a suitable subject.

Features

Add and manage subjects

Log study sessions

ML-based subject recommendation

Validation to prevent unknown subject predictions

Clean modal-based UI

SQLite database integration

How It Works

The model was trained using:

Mood

Focus level

Perceived difficulty

Hour of day

Weekday

Study duration

The predicted subject is verified against the user’s managed subjects before being displayed.

Tech Stack

Python, Flask, scikit-learn, Pandas, SQLite, HTML, CSS
