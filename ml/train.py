"""
Offline training and evaluation script for AI-IDPS.
Performs stratified 80/20 split on data/KDDTrain.txt, trains Decision Tree,
Random Forest (balanced), and XGBoost, saves Random Forest to models/model.pkl,
metrics to models/metrics.json, and PNG charts to static/charts/.
"""

import json
import os
import sys
from datetime import datetime

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ml.preprocess import fit_preprocessor, load_dataset, transform_features

TRAIN_PATH = os.path.join(ROOT_DIR, "data", "KDDTrain.txt")
MODEL_PATH = os.path.join(ROOT_DIR, "models", "model.pkl")
PREP_PATH = os.path.join(ROOT_DIR, "models", "preprocessor.pkl")
METRICS_PATH = os.path.join(ROOT_DIR, "models", "metrics.json")
CHARTS_DIR = os.path.join(ROOT_DIR, "static", "charts")

CLASS_ORDER = ["Normal", "DoS", "Probe", "R2L", "U2R"]


def compute_false_positive_rate(y_true, y_pred, normal_index):
    """Fraction of Normal records wrongly classified as attacks."""
    is_normal_true = (y_true == normal_index)
    is_attack_pred = (y_pred != normal_index)
    fp = int(np.sum(is_normal_true & is_attack_pred))
    tn = int(np.sum(is_normal_true & ~is_attack_pred))
    return fp / (fp + tn) if (fp + tn) > 0 else 0.0


def save_charts(class_counts, model_results, cm, class_names, rf_model, feature_names):
    """Generate and save the four evaluation charts as PNG images."""
    os.makedirs(CHARTS_DIR, exist_ok=True)
    plt.style.use("dark_background")

    # 1. Class distribution chart
    fig, ax = plt.subplots(figsize=(8, 4.8))
    labels = [c for c in CLASS_ORDER if c in class_counts]
    counts = [class_counts[c] for c in labels]
    colors = ["#22c55e", "#ef4444", "#f59e0b", "#38bdf8", "#a855f7"]
    bars = ax.bar(labels, counts, color=colors[:len(labels)], edgecolor="#1e293b")
    ax.set_title("NSL-KDD Training Class Distribution", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Number of Records")
    ax.grid(axis="y", alpha=0.2)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{count:,}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "class_distribution.png"), dpi=140, facecolor="#0f172a")
    plt.close(fig)

    # 2. Model comparison chart (Accuracy & F1-score)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    names = [m["algorithm"] for m in model_results]
    accs = [m["accuracy"] * 100 for m in model_results]
    f1s = [m["f1_score"] * 100 for m in model_results]
    x = np.arange(len(names))
    width = 0.34
    b1 = ax.bar(x - width / 2, accs, width, label="Accuracy (%)", color="#38bdf8")
    b2 = ax.bar(x + width / 2, f1s, width, label="Weighted F1 (%)", color="#22c55e")
    ax.set_title("Model Comparison (Accuracy vs Weighted F1-Score)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylim(min(90.0, min(accs + f1s) - 1.5), 100.5)
    ax.set_ylabel("Score (%)")
    ax.legend()
    ax.grid(axis="y", alpha=0.2)
    for bar in list(b1) + list(b2):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{bar.get_height():.2f}%", ha="center", va="bottom", fontsize=8.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "model_comparison.png"), dpi=140, facecolor="#0f172a")
    plt.close(fig)

    # 3. Random Forest Confusion Matrix
    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.figure.colorbar(im, ax=ax)
    ax.set(
        xticks=np.arange(len(class_names)),
        yticks=np.arange(len(class_names)),
        xticklabels=class_names,
        yticklabels=class_names,
        title="Random Forest Confusion Matrix",
        ylabel="Actual Class",
        xlabel="Predicted Class",
    )
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j, i, format(cm[i, j], "d"),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "#0f172a",
                fontsize=9.5, fontweight="bold"
            )
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "confusion_matrix.png"), dpi=140, facecolor="#0f172a")
    plt.close(fig)

    # 4. Top 10 Feature Importances (Random Forest)
    importances = rf_model.feature_importances_
    top_indices = np.argsort(importances)[-10:]
    top_names = [feature_names[i] for i in top_indices]
    top_vals = [importances[i] for i in top_indices]

    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    bars = ax.barh(top_names, top_vals, color="#38bdf8", edgecolor="#1e293b")
    ax.set_title("Top 10 Important Features (Random Forest)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Importance Score")
    ax.grid(axis="x", alpha=0.2)
    for bar, val in zip(bars, top_vals):
        ax.text(val + 0.002, bar.get_y() + bar.get_height() / 2,
                f"{val:.4f}", va="center", fontsize=8.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "feature_importance.png"), dpi=140, facecolor="#0f172a")
    plt.close(fig)


def train_and_evaluate():
    print("Loading training dataset:", TRAIN_PATH)
    df = load_dataset(TRAIN_PATH)
    print(f"Cleaned training records: {len(df)}")

    class_counts = df["label"].value_counts().to_dict()

    # Stratified 80/20 split before fitting scaler/encoders
    df_train, df_test = train_test_split(
        df, test_size=0.2, stratify=df["label"], random_state=42
    )

    X_train, y_train_labels, prep = fit_preprocessor(df_train, save_path=PREP_PATH)
    X_test = transform_features(df_test, prep)

    label_encoder = LabelEncoder()
    label_encoder.fit(CLASS_ORDER)
    y_train = label_encoder.transform(y_train_labels)
    y_test = label_encoder.transform(df_test["label"])

    class_names = list(label_encoder.classes_)
    normal_index = class_names.index("Normal")

    models = {
        "Decision Tree": DecisionTreeClassifier(
            class_weight="balanced", random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, class_weight="balanced", n_jobs=-1, random_state=42
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100, max_depth=6, learning_rate=0.1,
            eval_metric="mlogloss", n_jobs=-1, random_state=42
        ),
    }

    model_results = []
    trained_models = {}

    for name, clf in models.items():
        clf.fit(X_train, y_train)
        pred = clf.predict(X_test)
        acc = float(accuracy_score(y_test, pred))
        p, r, f1, _ = precision_recall_fscore_support(
            y_test, pred, average="weighted", zero_division=0
        )
        fpr = compute_false_positive_rate(y_test, pred, normal_index)

        print(
            f"{name}: accuracy={acc:.4f} precision={p:.4f} "
            f"recall={r:.4f} f1={f1:.4f} fpr={fpr:.4f}"
        )

        trained_models[name] = (clf, pred)
        model_results.append({
            "algorithm": name,
            "accuracy": round(acc, 6),
            "precision": round(float(p), 6),
            "recall": round(float(r), 6),
            "f1_score": round(float(f1), 6),
            "false_positive_rate": round(float(fpr), 6),
        })

    # Deploy Random Forest as the selected detection engine
    rf_model, rf_pred = trained_models["Random Forest"]
    print("\nClassification Report (Random Forest):")
    print(classification_report(y_test, rf_pred, target_names=class_names, zero_division=0))

    cm = confusion_matrix(y_test, rf_pred)
    print("Confusion Matrix (Random Forest):")
    print(cm)

    report_dict = classification_report(
        y_test, rf_pred, target_names=class_names, output_dict=True, zero_division=0
    )
    per_class_report = {}
    for cls in class_names:
        per_class_report[cls] = {
            "precision": round(float(report_dict[cls]["precision"]), 4),
            "recall": round(float(report_dict[cls]["recall"]), 4),
            "f1_score": round(float(report_dict[cls]["f1-score"]), 4),
            "support": int(report_dict[cls]["support"]),
        }

    # Top 10 features from Random Forest
    feature_names = prep["columns"]
    importances = rf_model.feature_importances_
    top_indices = np.argsort(importances)[::-1][:10]
    top_features = [
        {"feature": feature_names[i], "importance": round(float(importances[i]), 5)}
        for i in top_indices
    ]

    # Save Random Forest bundle
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(
        {"model": rf_model, "labels": class_names, "feature_names": feature_names},
        MODEL_PATH
    )
    print(f"\nSaved Random Forest model to {MODEL_PATH}")

    # Save metrics JSON
    trained_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metrics_payload = {
        "selected_model": "Random Forest",
        "trained_on": trained_on,
        "train_records": int(len(df_train)),
        "test_records": int(len(df_test)),
        "total_clean_records": int(len(df)),
        "class_distribution": {k: int(v) for k, v in class_counts.items()},
        "models": model_results,
        "random_forest_per_class": per_class_report,
        "labels": class_names,
        "confusion_matrix": cm.tolist(),
        "top_features": top_features,
    }
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"Saved metrics to {METRICS_PATH}")

    # Save PNG charts
    save_charts(class_counts, model_results, cm, class_names, rf_model, feature_names)
    print(f"Saved PNG charts to {CHARTS_DIR}")


if __name__ == "__main__":
    train_and_evaluate()