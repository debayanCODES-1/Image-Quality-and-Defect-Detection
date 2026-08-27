from __future__ import annotations

import os
from typing import Any, Dict, List

import joblib
import numpy as np

from .features import FEATURE_NAMES, extract_features

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "model")
MODEL_DIR = os.path.abspath(MODEL_DIR)


class QualityAnalyzer:
    def __init__(self) -> None:
        self.classifier_path = os.path.join(MODEL_DIR, "quality_clf.pkl")
        self.issue_path = os.path.join(MODEL_DIR, "issue_models.pkl")
        self.feature_names = FEATURE_NAMES

        self.classifier = None
        self.issue_models = {}
        self._load_models()

    def _load_models(self) -> None:
        if os.path.exists(self.classifier_path):
            self.classifier = joblib.load(self.classifier_path)
        if os.path.exists(self.issue_path):
            self.issue_models = joblib.load(self.issue_path)

    def analyze(self, image_bgr: np.ndarray) -> Dict[str, Any]:
        features = extract_features(image_bgr)
        X = np.array([features[name] for name in self.feature_names], dtype=float).reshape(1, -1)

        if self.classifier is not None:
            label = str(self.classifier.predict(X)[0])
            probs = self.classifier.predict_proba(X)[0]
            classes = self.classifier.classes_
            probs_map = dict(zip(classes, probs))
            score = int(round(float(probs_map.get("ACCEPTABLE", 0.5)) * 100))
        else:
            label = "ACCEPTABLE"
            score = 75

        issues: List[Dict[str, Any]] = []
        if self.issue_models:
            for issue, model in self.issue_models.items():
                estimate = float(model.predict(X)[0])
                if estimate > 0.5:
                    severity = "low" if estimate < 1.5 else "medium" if estimate < 2.5 else "high"
                    confidence = float(min(0.95, max(0.4, estimate / 3.0 + 0.45)))
                    issues.append({
                        "type": issue,
                        "severity": severity,
                        "confidence": round(confidence, 2),
                    })

        if not issues:
            issues = [{"type": "none", "severity": "low", "confidence": 0.5}]

        return {
            "quality_score": max(0, min(100, score)),
            "quality_label": label,
            "issues": issues,
            "features": features,
            "model_status": "trained" if self.classifier is not None else "fallback",
        }


analyzer = QualityAnalyzer()
