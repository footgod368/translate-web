CREATE TABLE IF NOT EXISTS query_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                word TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT
            )