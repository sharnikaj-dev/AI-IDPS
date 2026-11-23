"""
Main Flask web application for AI-IDPS.
Handles authentication, traffic replay from data/KDDTest.txt,
threat detection, automated prevention, and REST/JSON APIs.
"""

import csv
import io
import json
import os
import random
import sqlite3
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask,
    Response,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import DB_FILE, METRICS_FILE, init_db, sync_model_info
from ml.detect import predict
from ml.preprocess import load_dataset
from prevent import apply_action, get_thresholds, set_thresholds

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(BASE_DIR, "data", "KDDTest.txt")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ai-idps-mca-mini-project-secret-key")

# In-memory replay state for simulated live traffic
stream = {
    "data": None,
    "pos": 0,
    "total": 0,
    "running": False,
    "speed_ms": 1000,
    "batch_size": 5,
    "source": "data/KDDTest.txt",
}

# Pool of realistic external/LAN source IPs and internal destination server IPs
SRC_IP_POOL = (
    [f"192.168.{s}.{h}" for s in (1, 2, 3, 4) for h in range(10, 40)]
    + [f"172.16.{s}.{h}" for s in (1, 4, 8) for h in range(5, 25)]
    + [f"203.0.113.{h}" for h in range(12, 42)]
    + [f"198.51.100.{h}" for h in range(15, 45)]
)
DST_IP_POOL = [f"10.0.0.{h}" for h in range(5, 30)]


def get_db():
    """Return per-request SQLite connection stored on flask.g."""
    if "db" not in g:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def login_required(view):
    """Protect pages and JSON routes behind active session login."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify(error="Authentication required"), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def random_src_ip():
    return random.choice(SRC_IP_POOL)


def random_dst_ip():
    return random.choice(DST_IP_POOL)


def load_metrics_json():
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def ensure_stream_loaded():
    if stream["data"] is None:
        if not os.path.exists(TEST_DATA_PATH):
            raise FileNotFoundError(f"Dataset not found at {TEST_DATA_PATH}")
        stream["data"] = load_dataset(TEST_DATA_PATH).reset_index(drop=True)
        stream["total"] = len(stream["data"])


# ---------------- Authentication Routes ----------------

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            return render_template(
                "register.html",
                error="All fields are required.",
                form_data={"username": username, "email": email},
            )

        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match.",
                form_data={"username": username, "email": email},
            )

        if len(password) < 6:
            return render_template(
                "register.html",
                error="Password must be at least 6 characters long.",
                form_data={"username": username, "email": email},
            )

        db = get_db()
        # First registered user becomes admin; others become analyst
        user_count = db.execute("SELECT COUNT(*) AS cnt FROM users").fetchone()["cnt"]
        role = "admin" if user_count == 0 else "analyst"

        try:
            cur = db.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                (username, email, generate_password_hash(password), role),
            )
            db.commit()
            if role == "admin":
                sync_model_info(db, user_id=cur.lastrowid)
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="An account with this email address already exists.",
                form_data={"username": username, "email": email},
            )

        return redirect(url_for("login", registered=1))

    return render_template("register.html", form_data={})


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    success = "Account created successfully. Please sign in." if request.args.get("registered") else None

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["email"] = user["email"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password.",
            email=email,
        )

    return render_template("login.html", success=success)


@app.route("/logout")
def logout():
    stream["running"] = False
    session.clear()
    return redirect(url_for("login"))


# ---------------- Dashboard Page Routes ----------------

@app.route("/monitor")
@login_required
def monitor_start():
    thresholds = get_thresholds()
    metrics = load_metrics_json()
    active_model = metrics.get("selected_model", "Random Forest") if metrics else "Random Forest"
    return render_template(
        "monitor_start.html",
        active_page="monitor",
        running=stream["running"],
        pos=stream["pos"],
        total=stream["total"],
        speed_ms=stream["speed_ms"],
        batch_size=stream["batch_size"],
        block_threshold=thresholds["block_threshold"],
        limit_threshold=thresholds["limit_threshold"],
        active_model=active_model,
    )


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        active_page="dashboard",
        running=stream["running"],
        speed_ms=stream["speed_ms"],
    )


@app.route("/live")
@login_required
def live():
    db = get_db()
    recent_rows = db.execute(
        """
        SELECT t.log_id, t.src_ip, t.dst_ip, t.protocol, t.service,
               t.src_bytes, t.dst_bytes, t.logged_at,
               COALESCE(a.attack_type, 'Normal') AS prediction,
               COALESCE(a.confidence, 1.0) AS confidence,
               COALESCE(a.severity, 'LOW') AS severity,
               COALESCE(a.action_taken, 'Logged') AS action_taken
        FROM traffic_logs t
        LEFT JOIN alerts a ON t.log_id = a.log_id
        ORDER BY t.log_id DESC
        LIMIT 25
        """
    ).fetchall()
    return render_template(
        "live.html",
        active_page="live",
        running=stream["running"],
        pos=stream["pos"],
        total=stream["total"],
        speed_ms=stream["speed_ms"],
        recent_rows=recent_rows,
    )


@app.route("/alerts")
@login_required
def alerts():
    severity = request.args.get("severity", "ALL").upper()
    db = get_db()
    if severity in ("HIGH", "MEDIUM", "LOW"):
        rows = db.execute(
            """
            SELECT a.*, t.src_ip, t.dst_ip, t.protocol, t.service
            FROM alerts a
            JOIN traffic_logs t ON a.log_id = t.log_id
            WHERE a.severity = ?
            ORDER BY a.alert_id DESC
            LIMIT 200
            """,
            (severity,),
        ).fetchall()
    else:
        severity = "ALL"
        rows = db.execute(
            """
            SELECT a.*, t.src_ip, t.dst_ip, t.protocol, t.service
            FROM alerts a
            JOIN traffic_logs t ON a.log_id = t.log_id
            ORDER BY a.alert_id DESC
            LIMIT 200
            """
        ).fetchall()

    return render_template(
        "alerts.html",
        active_page="alerts",
        alerts=rows,
        selected_severity=severity,
    )


@app.route("/blocked")
@login_required
def blocked():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM blocked_ips ORDER BY block_id DESC"
    ).fetchall()
    return render_template(
        "blocked.html",
        active_page="blocked",
        blocked_list=rows,
    )


@app.route("/model")
@login_required
def model_performance():
    db = get_db()
    sync_model_info(db)
    model_rows = db.execute(
        "SELECT * FROM model_info ORDER BY model_id ASC"
    ).fetchall()
    metrics = load_metrics_json()
    return render_template(
        "model.html",
        active_page="model",
        model_rows=model_rows,
        metrics=metrics,
    )


@app.route("/reports")
@login_required
def reports():
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    return render_template(
        "reports.html",
        active_page="reports",
        default_start=week_ago,
        default_end=today,
    )


# ---------------- JSON & CSV API Routes ----------------

@app.route("/api/start", methods=["POST"])
@login_required
def api_start():
    payload = request.get_json(silent=True) or {}
    try:
        ensure_stream_loaded()
    except FileNotFoundError as exc:
        return jsonify(error=str(exc)), 404

    if payload.get("reset", False) or stream["pos"] >= stream["total"]:
        stream["pos"] = 0

    if "speed_ms" in payload:
        stream["speed_ms"] = max(250, min(5000, int(payload["speed_ms"])))
    if "batch_size" in payload:
        stream["batch_size"] = max(1, min(20, int(payload["batch_size"])))

    block_t = payload.get("block_threshold")
    limit_t = payload.get("limit_threshold")
    if block_t is not None or limit_t is not None:
        set_thresholds(block_t, limit_t)

    stream["running"] = True
    thresholds = get_thresholds()
    return jsonify(
        status="running",
        pos=stream["pos"],
        total=stream["total"],
        speed_ms=stream["speed_ms"],
        batch_size=stream["batch_size"],
        block_threshold=thresholds["block_threshold"],
        limit_threshold=thresholds["limit_threshold"],
    )


@app.route("/api/stop", methods=["POST"])
@login_required
def api_stop():
    stream["running"] = False
    return jsonify(status="stopped", pos=stream["pos"], total=stream["total"])


@app.route("/api/next")
@login_required
def api_next():
    if not stream["running"]:
        return jsonify(results=[], position=stream["pos"], total=stream["total"], running=False)

    try:
        ensure_stream_loaded()
    except FileNotFoundError as exc:
        stream["running"] = False
        return jsonify(error=str(exc), results=[], running=False), 404

    if stream["pos"] >= stream["total"]:
        stream["running"] = False
        return jsonify(results=[], position=stream["pos"], total=stream["total"], running=False)

    start = stream["pos"]
    batch_size = stream["batch_size"]
    batch = stream["data"].iloc[start:start + batch_size]
    stream["pos"] += len(batch)

    if stream["pos"] >= stream["total"]:
        stream["running"] = False

    db = get_db()
    results = []
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        for _, row in batch.iterrows():
            record = row.drop("label").to_dict()
            label, confidence = predict(record)
            src_ip = random_src_ip()
            dst_ip = random_dst_ip()
            protocol = str(record["protocol_type"])
            service = str(record["service"])
            src_bytes = int(record["src_bytes"])
            dst_bytes = int(record["dst_bytes"])

            cur = db.execute(
                """
                INSERT INTO traffic_logs
                (user_id, src_ip, dst_ip, protocol, service, src_bytes, dst_bytes, logged_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (session["user_id"], src_ip, dst_ip, protocol, service, src_bytes, dst_bytes, now_str),
            )
            log_id = cur.lastrowid
            action, severity = apply_action(
                db, log_id, src_ip, label, confidence, timestamp=now_str
            )

            results.append({
                "log_id": log_id,
                "time": now_str,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": protocol,
                "service": service,
                "src_bytes": src_bytes,
                "dst_bytes": dst_bytes,
                "prediction": label,
                "confidence": round(confidence * 100, 1),
                "severity": severity,
                "action": action,
            })
        db.commit()
    except FileNotFoundError as exc:
        stream["running"] = False
        return jsonify(error=str(exc), results=[], running=False), 500

    return jsonify(
        results=results,
        position=stream["pos"],
        total=stream["total"],
        running=stream["running"],
    )


@app.route("/api/stats")
@login_required
def api_stats():
    db = get_db()

    flows_analysed = db.execute("SELECT COUNT(*) AS c FROM traffic_logs").fetchone()["c"]
    threats_detected = db.execute("SELECT COUNT(*) AS c FROM alerts").fetchone()["c"]
    blocked_ips = db.execute(
        "SELECT COUNT(*) AS c FROM blocked_ips WHERE status = 'Blocked'"
    ).fetchone()["c"]

    rf_row = db.execute(
        "SELECT accuracy FROM model_info WHERE algorithm = 'Random Forest' ORDER BY model_id DESC LIMIT 1"
    ).fetchone()
    if rf_row:
        model_accuracy = round(rf_row["accuracy"] * 100, 2)
    else:
        metrics = load_metrics_json()
        model_accuracy = 0.0
        if metrics:
            for m in metrics.get("models", []):
                if m["algorithm"] == "Random Forest":
                    model_accuracy = round(m["accuracy"] * 100, 2)

    # Attack breakdown counts
    attack_counts = {"DoS": 0, "Probe": 0, "R2L": 0, "U2R": 0}
    for row in db.execute(
        "SELECT attack_type, COUNT(*) AS cnt FROM alerts GROUP BY attack_type"
    ).fetchall():
        if row["attack_type"] in attack_counts:
            attack_counts[row["attack_type"]] = row["cnt"]

    # Traffic timeline grouped into recent time buckets (up to last 12 buckets)
    timeline_rows = db.execute(
        """
        SELECT strftime('%H:%M:%S', t.logged_at) AS bucket,
               SUM(CASE WHEN a.alert_id IS NULL THEN 1 ELSE 0 END) AS normal_cnt,
               SUM(CASE WHEN a.alert_id IS NOT NULL THEN 1 ELSE 0 END) AS attack_cnt
        FROM traffic_logs t
        LEFT JOIN alerts a ON t.log_id = a.log_id
        GROUP BY bucket
        ORDER BY t.logged_at DESC
        LIMIT 12
        """
    ).fetchall()
    timeline_rows = list(reversed(timeline_rows))

    recent_alerts = [
        dict(r)
        for r in db.execute(
            """
            SELECT a.alert_id, a.attack_type, a.confidence, a.severity,
                   a.action_taken, a.alert_time, t.src_ip, t.service
            FROM alerts a
            JOIN traffic_logs t ON a.log_id = t.log_id
            ORDER BY a.alert_id DESC
            LIMIT 8
            """
        ).fetchall()
    ]

    return jsonify(
        flows_analysed=flows_analysed,
        threats_detected=threats_detected,
        blocked_ips=blocked_ips,
        model_accuracy=model_accuracy,
        running=stream["running"],
        position=stream["pos"],
        total=stream["total"],
        speed_ms=stream["speed_ms"],
        attack_counts=attack_counts,
        timeline={
            "labels": [r["bucket"] for r in timeline_rows],
            "normal": [r["normal_cnt"] for r in timeline_rows],
            "attack": [r["attack_cnt"] for r in timeline_rows],
        },
        recent_alerts=recent_alerts,
    )


@app.route("/api/alerts")
@login_required
def api_alerts():
    severity = request.args.get("severity", "ALL").upper()
    db = get_db()
    if severity in ("HIGH", "MEDIUM", "LOW"):
        rows = db.execute(
            """
            SELECT a.*, t.src_ip, t.dst_ip, t.protocol, t.service
            FROM alerts a
            JOIN traffic_logs t ON a.log_id = t.log_id
            WHERE a.severity = ?
            ORDER BY a.alert_id DESC
            LIMIT 200
            """,
            (severity,),
        ).fetchall()
    else:
        rows = db.execute(
            """
            SELECT a.*, t.src_ip, t.dst_ip, t.protocol, t.service
            FROM alerts a
            JOIN traffic_logs t ON a.log_id = t.log_id
            ORDER BY a.alert_id DESC
            LIMIT 200
            """
        ).fetchall()

    return jsonify(alerts=[dict(r) for r in rows])


@app.route("/api/blocked")
@login_required
def api_blocked():
    db = get_db()
    rows = db.execute("SELECT * FROM blocked_ips ORDER BY block_id DESC").fetchall()
    return jsonify(blocked=[dict(r) for r in rows])


@app.route("/api/unblock/<int:block_id>", methods=["POST"])
@login_required
def api_unblock(block_id):
    db = get_db()
    db.execute(
        "UPDATE blocked_ips SET status = 'Unblocked' WHERE block_id = ?",
        (block_id,),
    )
    db.commit()
    return jsonify(status="Unblocked", block_id=block_id)


@app.route("/api/reblock/<int:block_id>", methods=["POST"])
@login_required
def api_reblock(block_id):
    db = get_db()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.execute(
        "UPDATE blocked_ips SET status = 'Blocked', blocked_at = ? WHERE block_id = ?",
        (now, block_id),
    )
    db.commit()
    return jsonify(status="Blocked", block_id=block_id, blocked_at=now)


@app.route("/api/models")
@login_required
def api_models():
    db = get_db()
    sync_model_info(db)
    model_rows = [
        dict(r) for r in db.execute("SELECT * FROM model_info ORDER BY model_id ASC").fetchall()
    ]
    return jsonify(models=model_rows, metrics=load_metrics_json())


def build_report_data(db, start_date, end_date):
    """Query traffic_logs and alerts within [start_date, end_date] inclusive."""
    start_ts = f"{start_date} 00:00:00"
    end_ts = f"{end_date} 23:59:59"

    total_flows = db.execute(
        "SELECT COUNT(*) AS c FROM traffic_logs WHERE logged_at BETWEEN ? AND ?",
        (start_ts, end_ts),
    ).fetchone()["c"]

    rows = db.execute(
        """
        SELECT attack_type,
               COUNT(*) AS detected,
               SUM(CASE WHEN action_taken = 'Blocked' THEN 1 ELSE 0 END) AS blocked,
               SUM(CASE WHEN action_taken = 'Rate-limited' THEN 1 ELSE 0 END) AS rate_limited,
               SUM(CASE WHEN action_taken = 'Logged' THEN 1 ELSE 0 END) AS logged
        FROM alerts
        WHERE alert_time BETWEEN ? AND ?
        GROUP BY attack_type
        """,
        (start_ts, end_ts),
    ).fetchall()

    by_class = {r["attack_type"]: dict(r) for r in rows}
    breakdown = []
    totals = {"detected": 0, "blocked": 0, "rate_limited": 0, "logged": 0}

    for cls in ("DoS", "Probe", "R2L", "U2R"):
        item = by_class.get(
            cls, {"attack_type": cls, "detected": 0, "blocked": 0, "rate_limited": 0, "logged": 0}
        )
        entry = {
            "attack_type": cls,
            "detected": int(item["detected"] or 0),
            "blocked": int(item["blocked"] or 0),
            "rate_limited": int(item["rate_limited"] or 0),
            "logged": int(item["logged"] or 0),
        }
        breakdown.append(entry)
        totals["detected"] += entry["detected"]
        totals["blocked"] += entry["blocked"]
        totals["rate_limited"] += entry["rate_limited"]
        totals["logged"] += entry["logged"]

    return {
        "start": start_date,
        "end": end_date,
        "total_flows": int(total_flows),
        "total_threats": totals["detected"],
        "total_blocked": totals["blocked"],
        "total_rate_limited": totals["rate_limited"],
        "total_logged": totals["logged"],
        "breakdown": breakdown,
    }


@app.route("/api/report")
@login_required
def api_report():
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    start_date = request.args.get("start") or week_ago
    end_date = request.args.get("end") or today

    db = get_db()
    return jsonify(build_report_data(db, start_date, end_date))


@app.route("/api/report/csv")
@login_required
def api_report_csv():
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    start_date = request.args.get("start") or week_ago
    end_date = request.args.get("end") or today

    db = get_db()
    report = build_report_data(db, start_date, end_date)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["AI-IDPS Threat Summary Report"])
    writer.writerow(["Period Start", report["start"], "Period End", report["end"]])
    writer.writerow(["Total Flows Analysed", report["total_flows"]])
    writer.writerow([])
    writer.writerow(["Attack Class", "Detected", "Blocked", "Rate-limited", "Logged"])
    for row in report["breakdown"]:
        writer.writerow([
            row["attack_type"],
            row["detected"],
            row["blocked"],
            row["rate_limited"],
            row["logged"],
        ])
    writer.writerow([
        "Total",
        report["total_threats"],
        report["total_blocked"],
        report["total_rate_limited"],
        report["total_logged"],
    ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=ai_idps_report_{start_date}_to_{end_date}.csv"
        },
    )


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)