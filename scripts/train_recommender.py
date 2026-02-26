# src/train_recommender.py
import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from src.database import get_all_sessions

OUT_DIR = os.path.join(os.path.dirname(__file__), "ml")
os.makedirs(OUT_DIR, exist_ok=True)
MODEL_PATH = os.path.join(OUT_DIR, "recommender.pkl")
ENC_PATH = os.path.join(OUT_DIR, "label_encoder.pkl")

def prepare_features(df):
    # ensure relevant columns exist
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce', infer_datetime_format=True)
    df['hour'] = df['date'].dt.hour.fillna(12).astype(int)  # default 12 if time missing
    df['weekday'] = df['date'].dt.weekday
    df['perceived_difficulty'] = df.get('perceived_difficulty', pd.Series(3, index=df.index)).fillna(3).astype(int)
    df['focus_level'] = df.get('focus_level', pd.Series(3, index=df.index)).fillna(3).astype(int)
    df['mood'] = df.get('mood', pd.Series(3, index=df.index)).fillna(3).astype(int)
    df['duration_minutes'] = df.get('duration_minutes', pd.Series(30, index=df.index)).fillna(30).astype(int)

    feature_cols = ['mood', 'focus_level', 'perceived_difficulty', 'hour', 'weekday', 'duration_minutes']
    X = df[feature_cols]
    y = df['subject']
    return X, y, feature_cols

def train_and_persist():
    df = get_all_sessions()
    if df is None or df.empty:
        print("No data to train on. Log some sessions first.")
        return

    # minimal check: need at least 2 subjects and some rows
    if df['subject'].nunique() < 2 or len(df) < 20:
        print("Not enough data to train a reliable model. Falling back to rule-based recommender.")
        return

    X, y, feature_order = prepare_features(df)

    # Encode labels
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f"Validation accuracy: {acc:.3f} on {len(y_test)} samples")

    # Persist model + metadata
    bundle = {
        "model": model,
        "feature_order": feature_order,
        "label_encoder": le
    }
    # We can't joblib.dump the whole bundle with label encoder as object mapping across versions may confuse.
    # Save model and encoder separately:
    joblib.dump({"model": model, "feature_order": feature_order}, MODEL_PATH)
    joblib.dump(le, ENC_PATH)
    print("Saved trained recommender to:", MODEL_PATH)
    print("Saved label encoder to:", ENC_PATH)

if __name__ == "__main__":
    train_and_persist()
    