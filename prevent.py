"""
Intelligent Prevention Engine.
Selects a proportionate response based on predicted class and confidence:
- Normal: Logged only (no alert)
- Attack with confidence >= block_threshold (default 0.90): Blocked / HIGH
- Attack with confidence >= limit_threshold (default 0.60): Rate-limited / MEDIUM
- Attack with confidence < limit_threshold: Logged / LOW
"""

from datetime import datetime

DEFAULT_BLOCK_THRESHOLD = 0.90
DEFAULT_LIMIT_THRESHOLD = 0.60

_settings = {
    "block_threshold": DEFAULT_BLOCK_THRESHOLD,
    "limit_threshold": DEFAULT_LIMIT_THRESHOLD,
}


def get_thresholds():
    """Return current prevention thresholds."""
    return dict(_settings)


def set_thresholds(block_threshold=None, limit_threshold=None):
    """Adjust prevention thresholds safely."""
    b = _settings["block_threshold"] if block_threshold is None else float(block_threshold)
    l = _settings["limit_threshold"] if limit_threshold is None else float(limit_threshold)
    b = max(0.0, min(1.0, b))
    l = max(0.0, min(b, l))
    _settings["block_threshold"] = b
    _settings["limit_threshold"] = l
    return dict(_settings)


def decide(label, confidence, block_threshold=None, limit_threshold=None):
    """Determine (action, severity) for a prediction."""
    if label == "Normal":
        return "Logged", "LOW"

    b_thresh = _settings["block_threshold"] if block_threshold is None else float(block_threshold)
    l_thresh = _settings["limit_threshold"] if limit_threshold is None else float(limit_threshold)

    if confidence >= b_thresh:
        return "Blocked", "HIGH"
    if confidence >= l_thresh:
        return "Rate-limited", "MEDIUM"
    return "Logged", "LOW"


def apply_action(
    db,
    log_id,
    src_ip,
    label,
    confidence,
    block_threshold=None,
    limit_threshold=None,
    timestamp=None,
):
    """Apply prevention policy, update blocked_ips and alerts tables, return (action, severity)."""
    action, severity = decide(label, confidence, block_threshold, limit_threshold)
    now = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    block_id = None

    if label != "Normal":
        if action == "Blocked":
            existing = db.execute(
                "SELECT block_id FROM blocked_ips WHERE ip_address = ? AND status = 'Blocked'",
                (src_ip,),
            ).fetchone()
            if existing:
                block_id = existing["block_id"]
            else:
                cur = db.execute(
                    """
                    INSERT INTO blocked_ips (ip_address, reason, blocked_at, status)
                    VALUES (?, ?, ?, 'Blocked')
                    """,
                    (src_ip, label, now),
                )
                block_id = cur.lastrowid

        db.execute(
            """
            INSERT INTO alerts (log_id, block_id, attack_type, confidence, severity, action_taken, alert_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (log_id, block_id, label, round(float(confidence), 4), severity, action, now),
        )

    return action, severity