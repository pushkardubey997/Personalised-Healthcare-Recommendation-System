import os
import numpy as np
import joblib
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

_model = None
_encoder = None
_features: list[str] = []


def load_artifacts():
    """Load ML model, encoder, and feature list once at startup."""
    global _model, _encoder, _features

    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(base, os.getenv("MODEL_PATH", "ml_models/model.pkl"))
    encoder_path = os.path.join(base, os.getenv("ENCODER_PATH", "ml_models/encoder.pkl"))
    features_path = os.path.join(base, os.getenv("FEATURES_PATH", "ml_models/features.csv"))

    print(f"[ModelService] Loading model from {model_path}")
    _model = joblib.load(model_path)

    print(f"[ModelService] Loading encoder from {encoder_path}")
    _encoder = joblib.load(encoder_path)

    print(f"[ModelService] Loading features from {features_path}")
    df = pd.read_csv(features_path)
    _features = df["symptom"].tolist()

    print(f"[ModelService] Ready — {len(_features)} features, {len(_encoder.classes_)} diseases")


def get_features() -> list[str]:
    return _features


def predict(symptom_vector: list[int]) -> str:
    """Run prediction, return decoded disease name."""
    if _model is None or _encoder is None:
        raise RuntimeError("Model not loaded. Call load_artifacts() first.")

    arr = np.array(symptom_vector, dtype=np.int32).reshape(1, -1)
    raw_pred = _model.predict(arr)[0]
    disease_name = _encoder.inverse_transform([raw_pred])[0]
    return disease_name
