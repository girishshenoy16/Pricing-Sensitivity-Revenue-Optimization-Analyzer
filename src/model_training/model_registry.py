import joblib
import os
from src.config import MODEL_DIR

def save_model(model, category):
    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, f"{category}_model.pkl")
    joblib.dump(model, path)
    return path

def load_model(category):
    path = os.path.join(MODEL_DIR, f"{category}_model.pkl")
    return joblib.load(path)