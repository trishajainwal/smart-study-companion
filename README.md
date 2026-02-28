# 📚 Smart Study Companion

A full-stack **Flask** web application that intelligently recommends what subject to study based on behavioral patterns such as mood, focus level, and time-based features.

The application logs study sessions, stores data in a database, and uses a trained machine learning model to generate personalized subject suggestions.

---

## 🚀 Features

- 📌 Add and manage custom subjects  
- 📝 Log detailed study sessions  
- 🤖 ML-based subject recommendation  
- ✅ Validation to prevent unsupported predictions  
- 📊 Structured database logging (SQLite)  
- 🎨 Clean and responsive UI  
- 🔒 Safe and controlled prediction output  

---

## 🧠 Machine Learning Model

The recommendation model was trained using:

- Mood (1–5)
- Focus Level (1–5)
- Perceived Difficulty
- Hour of Day
- Weekday
- Study Duration

The predicted subject is validated against the user’s managed subject list before being displayed.

---

## 🏗 Tech Stack

**Backend**
- Python
- Flask

**Machine Learning**
- scikit-learn
- joblib

**Data Processing**
- Pandas

**Database**
- SQLite

**Frontend**
- HTML
- CSS

---


## 🔮 Future Improvements

- Per-user adaptive model training  
- Enhanced analytics dashboard  
- Improved recommendation accuracy  
- Deployment-ready configuration  

---

## 🎯 Learning Outcomes

This project demonstrates:

- Full-stack web development with Flask  
- Machine learning model integration into a live web application  
- Feature engineering and prediction pipelines  
- Database design and session logging  
- Modular backend architecture  


