import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from src.database import get_all_sessions  
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml", "recommender.pkl")
ENC_PATH = os.path.join(os.path.dirname(__file__), "ml", "label_encoder.pkl")

# Minimum training samples per subject to trust the learned model
MIN_SAMPLES_PER_SUBJECT = 5

def _rule_based_score(df, mood, focus, allowed_subjects):
    """
    Fallback scoring if model isn't available or data is tiny.
    Returns best_subject, reason, scores dict.
    """
    if df.empty:
        return None, "No past data yet — add a couple of sessions so I can learn.", {}

    scores = {}
    today = pd.Timestamp.today()
    all_subjects = [s for s in df['subject'].unique() if (not allowed_subjects) or (s in allowed_subjects)]
    if not all_subjects:
        # if no allowed subject present in DB, fallback to allowed_subjects list itself
        all_subjects = allowed_subjects or df['subject'].unique().tolist()

    for sub in all_subjects:
        sub_df = df[df['subject'] == sub]
        mood_sim = 1 - min(1, abs(sub_df["mood"].mean() - mood) / 5) if not sub_df.empty else 0.0
        focus_sim = 1 - min(1, abs(sub_df["focus_level"].mean() - focus) / 5) if not sub_df.empty else 0.0

        # recency: more recent -> smaller days_since -> bigger score
        if not sub_df.empty:
            last_days = (today - pd.to_datetime(sub_df["date"])).dt.days.min()
            recency_score = 1 / (1 + last_days)
        else:
            recency_score = 0.01

        score = 0.45 * mood_sim + 0.45 * focus_sim + 0.10 * recency_score
        scores[sub] = score

    best = max(scores, key=scores.get)
    reason = "Based on past mood/focus matches and recency."
    return best, reason, scores

def recommend_subject(mood, focus, allowed_subjects=None):
    """
    Top-level function used by Flask.
    - mood, focus: ints (1-5)
    - allowed_subjects: list of subjects that can be recommended (from app MY_SUBJECTS)
    Returns dict: {subject, reason, confidence}
    """
    # Load DB
    df = get_all_sessions()

    # If no data, fallback immediately
    if df is None or df.empty:
        best, reason, scores = _rule_based_score(pd.DataFrame(), mood, focus, allowed_subjects or [])
        return {"subject": best, "reason": reason, "confidence": 0.0, "scores": scores}

    # Count samples per subject
    counts = df['subject'].value_counts().to_dict()
    # If dataset too small per subject, use rule-based fallback
    too_small = any(v < MIN_SAMPLES_PER_SUBJECT for v in counts.values()) and len(counts) < 4

    # Try to load model
    if os.path.exists(MODEL_PATH) and not too_small:
        try:
            model_bundle = joblib.load(MODEL_PATH)
            model = model_bundle['model']
            enc = joblib.load(ENC_PATH) if os.path.exists(ENC_PATH) else None

            # Build a single-row feature vector consistent with training:
            # features used in training: mood, focus_level, perceived_difficulty, hour, weekday, duration_minutes
            now = datetime.now()
            feat = {
                "mood": mood,
                "focus_level": focus,
                # use median values for other features (safe defaults) or compute from df
                "perceived_difficulty": int(df['perceived_difficulty'].median() if 'perceived_difficulty' in df.columns and not df['perceived_difficulty'].isnull().all() else 3),
                "hour": now.hour,
                "weekday": now.weekday(),
                "duration_minutes": int(df['duration_minutes'].median() if 'duration_minutes' in df.columns and not df['duration_minutes'].isnull().all() else 30)
            }

            X = pd.DataFrame([feat])[model_bundle['feature_order']]

            proba = None
            pred = None
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(X)[0]
                classes = model.classes_
                # convert to dict of subject->prob
                prob_dict = {classes[i]: float(probs[i]) for i in range(len(classes))}
                # filter by allowed_subjects if provided
                if allowed_subjects:
                    prob_dict = {k: v for k, v in prob_dict.items() if k in allowed_subjects}
                if not prob_dict:
                    # no allowed subjects in model classes -> fallback
                    raise Exception("No allowed subject in trained classes")
                pred = max(prob_dict, key=prob_dict.get)
                confidence = prob_dict[pred]
                return {"subject": pred, "reason": "Model prediction (trained on your history).", "confidence": float(confidence), "scores": prob_dict}
            else:
                pred = model.predict(X)[0]
                if allowed_subjects and pred not in allowed_subjects:
                    # try to choose best allowed via rule-based fallback
                    raise Exception("Predicted subject not in allowed list")
                return {"subject": pred, "reason": "Model prediction (no probabilities available).", "confidence": 1.0, "scores": {}}

        except Exception as e:
            # any failure -> fallback to rule-based
            print("Model load/predict failed:", e)

    # Fallback to rule-based scoring
    best, reason, scores = _rule_based_score(df, mood, focus, allowed_subjects or [])
    # compute a naive confidence from relative score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    confidence = float(sorted_scores[0][1]) if sorted_scores else 0.0
    return {"subject": best, "reason": reason + " (fallback)", "confidence": confidence, "scores": scores}
