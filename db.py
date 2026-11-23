"""
SQLite database connection, schema initialization, and metrics synchronization.
"""

import json
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "idps.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")
METRICS_FILE = os.path.join(BASE_DIR, "models", "metrics.json")

FALLBACK_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'analyst',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS traffic_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    src_ip TEXT,
    dst_ip TEXT,
    protocol TEXT,
    service TEXT,
    src_bytes INTEGER,
    dst_bytes INTEGER,
    logged_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blocked_ips (
    block_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    reason TEXT,
    blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Blocked'
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER REFERENCES traffic_logs(log_id),
    block_id INTEGER REFERENCES blocked_ips(block_id),
    attack_type TEXT,
    confidence REAL,
    severity TEXT,
    action_taken TEXT,
    alert_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_info (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    algorithm TEXT,
    accuracy REAL,
    f1_score REAL,
    trained_on DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection():
    """Return a configured SQLite connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables from schema.sql and load models/metrics.json into model_info."""
    conn = get_connection()
    try:
        if os.path.exists(SCHEMA_FILE):
            with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                schema_sql = f.read()
        else:
            schema_sql = FALLBACK_SCHEMA
        conn.executescript(schema_sql)
        conn.commit()
        sync_model_info(conn)
    finally:
        conn.close()


def sync_model_info(conn=None, user_id=None):
    """Load models/metrics.json into the model_info table if available."""
    if not os.path.exists(METRICS_FILE):
        return

    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    models = metrics.get("models", [])
    trained_on = metrics.get("trained_on")
    if not models:
        return

    own_conn = False
    if conn is None:
        conn = get_connection()
        own_conn = True

    try:
        if user_id is None:
            user_row = conn.execute(
                "SELECT user_id FROM users ORDER BY user_id ASC LIMIT 1"
            ).fetchone()
            user_id = user_row["user_id"] if user_row else None

        existing = conn.execute(
            "SELECT COUNT(*) AS cnt FROM model_info WHERE trained_on = ?",
            (trained_on,)
        ).fetchone()["cnt"]

        if existing == 0:
            conn.execute("DELETE FROM model_info")
            for m in models:
                conn.execute(
                    """
                    INSERT INTO model_info (user_id, algorithm, accuracy, f1_score, trained_on)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        m["algorithm"],
                        float(m["accuracy"]),
                        float(m["f1_score"]),
                        trained_on,
                    ),
                )
            conn.commit()
    finally:
        if own_conn:
            conn.close()