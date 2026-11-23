"""
Seeds a demo admin account and replays a short batch of NSL-KDD test records
into idps.db so the dashboard, alerts, blocked IPs, and reports are populated
immediately for demonstration and screenshots.
"""

import os
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

from db import get_connection, init_db, sync_model_info
from ml.detect import predict
from ml.preprocess import load_dataset
from prevent import apply_action

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(BASE_DIR, "data", "KDDTest.txt")

DEMO_ADMIN = {
    "username": "Sharnika J",
    "email": "admin@aiidps.local",
    "password": "admin123",
}


def seed():
    init_db()
    conn = get_connection()
    try:
        # 1. Create demo admin user if not present
        user = conn.execute(
            "SELECT user_id FROM users WHERE email = ?", (DEMO_ADMIN["email"],)
        ).fetchone()
        if user:
            user_id = user["user_id"]
        else:
            cur = conn.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, 'admin')",
                (
                    DEMO_ADMIN["username"],
                    DEMO_ADMIN["email"],
                    generate_password_hash(DEMO_ADMIN["password"]),
                ),
            )
            user_id = cur.lastrowid
            conn.commit()
            print(f"Created demo admin: {DEMO_ADMIN['email']} / {DEMO_ADMIN['password']}")

        sync_model_info(conn, user_id=user_id)

        # 2. Replay 60 records from KDDTest.txt for sample screenshots
        df = load_dataset(TEST_DATA_PATH).head(60)
        src_pool = [f"192.168.1.{i}" for i in range(15, 45)] + [f"203.0.113.{i}" for i in range(10, 25)]
        dst_pool = [f"10.0.0.{i}" for i in range(5, 15)]

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _, row in df.iterrows():
            record = row.drop("label").to_dict()
            label, confidence = predict(record)
            src_ip = random.choice(src_pool)
            dst_ip = random.choice(dst_pool)

            cur = conn.execute(
                """
                INSERT INTO traffic_logs
                (user_id, src_ip, dst_ip, protocol, service, src_bytes, dst_bytes, logged_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    src_ip,
                    dst_ip,
                    str(record["protocol_type"]),
                    str(record["service"]),
                    int(record["src_bytes"]),
                    int(record["dst_bytes"]),
                    now_str,
                ),
            )
            apply_action(conn, cur.lastrowid, src_ip, label, confidence, timestamp=now_str)

        conn.commit()
        print(f"Seeded {len(df)} traffic flows into idps.db successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    seed()