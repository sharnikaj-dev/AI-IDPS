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