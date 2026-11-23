"""
Online threat detection module.
Loads models/model.pkl and models/preprocessor.pkl and predicts
the traffic class along with Random Forest vote-fraction confidence.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ml.preprocess import transform_features

MODEL_PATH = os.path.join(ROOT_DIR, "models", "model.pkl")
PREP_PATH = os.path.join(ROOT_DIR, "models", "preprocessor.pkl")

_bundle = None
_prep = None


def _load_artifacts():
    """Lazy-load trained Random Forest model and preprocessor."""
    global _bundle, _prep
    if _bundle is None or _prep is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(PREP_PATH):
            raise FileNotFoundError(
                "Trained model artifacts not found. Run 'python ml/train.py' first."
            )
        _bundle = joblib.load(MODEL_PATH)
        _prep = joblib.load(PREP_PATH)
    return _bundle, _prep


def predict(record):
    """
    Predict threat class and confidence (Random Forest tree vote fraction).
    Returns: (label: str, confidence: float in [0.0, 1.0])
    """
    bundle, prep = _load_artifacts()
    model = bundle["model"]
    labels = bundle["labels"]

    if isinstance(record, pd.Series):
        record_dict = record.to_dict()
    else:
        record_dict = dict(record)

    row_df = pd.DataFrame([record_dict])[prep["columns"]]
    x = transform_features(row_df, prep)

    # Random Forest predict_proba returns the mean vote fraction across all trees
    proba = model.predict_proba(x)[0]
    best_idx = int(np.argmax(proba))
    return str(labels[best_idx]), float(proba[best_idx])