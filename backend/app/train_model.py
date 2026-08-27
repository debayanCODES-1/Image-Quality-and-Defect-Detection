from __future__ import annotations

import os
from pathlib import Path

import cv2
import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.model_selection import train_test_split

from .features import FEATURE_NAMES, extract_features


DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "synthetic_dataset.csv"
MODEL_DIR = Path(__file__).resolve().parents[1] / "model"

ISSUE_COLUMNS = ["blur", "underexposure", "overexposure", "noise", "corruption"]


def add_blur(image: np.ndarray, sigma: float) -> np.ndarray:
    return cv2.GaussianBlur(image, (0, 0), sigmaX=sigma, sigmaY=sigma)


def add_noise(image: np.ndarray, sigma: float) -> np.ndarray:
    noise = np.random.normal(0, sigma, image.shape).astype(np.int16)
    noisy = image.astype(np.int16) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_underexposure(image: np.ndarray, factor: float) -> np.ndarray:
    return np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)


def add_overexposure(image: np.ndarray, factor: float) -> np.ndarray:
    return np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)


def apply_corruption(image: np.ndarray) -> np.ndarray:
    corrupted = image.copy()
    h, w = corrupted.shape[:2]
    for _ in range(4):
        x = np.random.randint(0, h)
        y = np.random.randint(0, w)
        block_h = np.random.randint(10, max(20, h // 6))
        block_w = np.random.randint(10, max(20, w // 6))
        corrupted[max(0, x - block_h // 2):min(h, x + block_h // 2), max(0, y - block_w // 2):min(w, y + block_w // 2)] = 0
    return corrupted


def generate_synthetic_sample(image: np.ndarray) -> tuple[np.ndarray, dict]:
    transform = np.random.choice(["blur", "noise", "under", "over", "corrupt", "mixed"])
    sample = image.copy()

    if transform == "blur":
        sample = add_blur(sample, float(np.random.uniform(1.5, 7.0)))
        issue = {"blur": 2, "underexposure": 0, "overexposure": 0, "noise": 0, "corruption": 0}
    elif transform == "noise":
        sample = add_noise(sample, float(np.random.uniform(10, 40)))
        issue = {"blur": 0, "underexposure": 0, "overexposure": 0, "noise": 2, "corruption": 0}
    elif transform == "under":
        sample = add_underexposure(sample, float(np.random.uniform(0.3, 0.6)))
        issue = {"blur": 0, "underexposure": 2, "overexposure": 0, "noise": 0, "corruption": 0}
    elif transform == "over":
        sample = add_overexposure(sample, float(np.random.uniform(1.3, 1.8)))
        issue = {"blur": 0, "underexposure": 0, "overexposure": 2, "noise": 0, "corruption": 0}
    elif transform == "corrupt":
        sample = apply_corruption(sample)
        issue = {"blur": 0, "underexposure": 0, "overexposure": 0, "noise": 0, "corruption": 2}
    else:
        sample = add_blur(sample, np.random.uniform(1.5, 5.0))
        sample = add_noise(sample, np.random.uniform(8, 30))
        issue = {"blur": 1, "underexposure": 1, "overexposure": 0, "noise": 1, "corruption": 0}

    quality_label = "ACCEPTABLE" if max(issue.values()) <= 1 else "DEGRADED" if max(issue.values()) <= 2 else "DEFECTIVE"
    quality_score = 95 if quality_label == "ACCEPTABLE" else 60 if quality_label == "DEGRADED" else 25
    return sample, {"quality_label": quality_label, "quality_score": quality_score, **issue}


def build_dataset(image_dir: str | os.PathLike[str]) -> pd.DataFrame:
    rows = []
    image_dir = Path(image_dir)
    if not image_dir.exists():
        raise FileNotFoundError(f"Image directory not found: {image_dir}")

    for image_path in sorted(image_dir.glob("*")):
        if image_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".bmp"}:
            continue
        image = cv2.imread(str(image_path))
        if image is None:
            continue

        for _ in range(3):
            synthetic, meta = generate_synthetic_sample(image)
            features = extract_features(synthetic)
            row = {**features, **meta}
            rows.append(row)

    if not rows:
        raise ValueError("No valid images were found for synthetic dataset creation.")

    return pd.DataFrame(rows)


def train_models(dataset_path: str | os.PathLike[str] | None = None) -> None:
    data_path = Path(dataset_path) if dataset_path else DATASET_PATH
    if not data_path.exists():
        raise FileNotFoundError(
            "Dataset not found. Add a CSV file or generate one from a clean image directory before training."
        )

    df = pd.read_csv(data_path)
    X = df[FEATURE_NAMES]
    y_label = df["quality_label"]
    y_score = df["quality_score"]
    y_issues = df[ISSUE_COLUMNS]

    X_train, X_test, y_train, y_test = train_test_split(X, y_label, test_size=0.2, random_state=42)
    clf = LGBMClassifier(objective="multiclass", num_class=3, n_estimators=200, learning_rate=0.05)
    clf.fit(X_train, y_train)

    issue_models = {}
    for issue in ISSUE_COLUMNS:
        model = LGBMRegressor(n_estimators=150, learning_rate=0.05)
        model.fit(X_train, y_issues[issue])
        issue_models[issue] = model

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_DIR / "quality_clf.pkl")
    joblib.dump(issue_models, MODEL_DIR / "issue_models.pkl")
    print(f"Saved model artifacts to {MODEL_DIR}")


if __name__ == "__main__":
    print("Synthetic training pipeline scaffold ready.")
    print("Use build_dataset() on a directory of clean images and then train_models().")
