📚 Smart Study Companion 

A Flask-based web application that recommends what subject to study based on your current mood and focus level.

Instead of randomly picking a topic, the system uses a trained machine learning model to suggest a subject that best fits your current state.

🚀 What It Does

Allows users to manage their own study subjects

Logs study session data

Uses an ML model to recommend a subject

Ensures recommendations match the user’s added subjects

Displays suggestions through a clean modal interface

Stores data locally using SQLite

🧠 How It Works

The model was trained using features such as:

Mood

Focus level

Perceived difficulty

Time of day

Day of the week

Study duration

Based on these inputs, the system predicts a subject and verifies that it exists in the user’s managed list before displaying it.

🛠 Built With

Python

Flask

scikit-learn

Pandas

SQLite

HTML & CSS
