"""
Data loading and preprocessing for the NSL-KDD dataset.
Cleans duplicates/nulls, maps all train & test attack labels to 5 classes,
encodes categorical fields safely for unseen values, and scales features.
"""

import os
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PREP_PATH = os.path.join(BASE_DIR, "models", "preprocessor.pkl")

# Standard 43 NSL-KDD column names (41 features + label + difficulty)
COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty"
]

# Complete attack-to-family mapping covering both KDDTrain and KDDTest attacks
FAMILIES = {
    "DoS": [
        "back", "land", "neptune", "pod", "smurf", "teardrop",
        "apache2", "udpstorm", "processtable", "worm", "mailbomb"
    ],
    "Probe": [
        "ipsweep", "nmap", "portsweep", "satan", "mscan", "saint"
    ],
    "R2L": [
        "ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy",
        "warezclient", "warezmaster", "sendmail", "named",
        "snmpgetattack", "snmpguess", "xlock", "xsnoop", "httptunnel"
    ],
    "U2R": [
        "buffer_overflow", "loadmodule", "perl", "rootkit",
        "ps", "sqlattack", "xterm"
    ],
}

ATTACK_MAP = {"normal": "Normal"}
for family, attack_names in FAMILIES.items():
    for attack_name in attack_names:
        ATTACK_MAP[attack_name] = family

CATEGORICAL_COLS = ["protocol_type", "service", "flag"]
FEATURE_COLS = [col for col in COLUMNS if col not in ("label", "difficulty")]


def load_dataset(path):
    """Load an NSL-KDD file, drop difficulty, map labels to 5 classes, and clean."""
    df = pd.read_csv(path, names=COLUMNS, header=None)
    df = df.drop(columns=["difficulty"])

    # Normalize label strings before mapping
    df["label"] = (
        df["label"]
        .astype(str)
        .str.strip()
        .str.rstrip(".")
        .str.lower()
        .map(ATTACK_MAP)
    )

    for col in CATEGORICAL_COLS:
        df[col] = df[col].astype(str).str.strip()

    # Remove missing/unmapped rows and duplicate records
    df = df.dropna().drop_duplicates().reset_index(drop=True)
    return df


# Alias kept for compatibility with spec appendix
load = load_dataset


def fit_preprocessor(df, save_path=DEFAULT_PREP_PATH):
    """Fit categorical mappings and StandardScaler on training data, then save."""
    X = df[FEATURE_COLS].copy()
    y = df["label"].copy()

    mappings = {}
    for col in CATEGORICAL_COLS:
        classes = sorted(X[col].astype(str).unique())
        mappings[col] = {val: idx for idx, val in enumerate(classes)}
        X[col] = X[col].astype(str).map(mappings[col]).fillna(-1).astype(int)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    prep_bundle = {
        "mappings": mappings,
        "scaler": scaler,
        "columns": list(X.columns),
    }
    joblib.dump(prep_bundle, save_path)
    return X_scaled, y, prep_bundle


def transform_features(df, prep):
    """Transform a DataFrame using saved mappings and scaler (safe for unseen values)."""
    X = df[prep["columns"]].copy()
    for col, mapping in prep["mappings"].items():
        X[col] = X[col].astype(str).str.strip().map(mapping).fillna(-1).astype(int)

    for col in prep["columns"]:
        if col not in prep["mappings"]:
            X[col] = pd.to_numeric(X[col], errors="coerce").fillna(0.0)

    return prep["scaler"].transform(X)