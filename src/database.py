import sqlite3
import os
from contextlib import closing
from flask import current_app
import datetime


def init_db(DATABASE_FILE):
    if os.path.exists(DATABASE_FILE):
        return
    with closing(sqlite3.connect(DATABASE_FILE)) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS query_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                word TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT
            )
        """
        )
        conn.commit()


def log_query(DATABASE_FILE, word, ip_address=None, user_agent=None):
    with closing(sqlite3.connect(DATABASE_FILE)) as conn:
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO query_log (word, ip_address, user_agent)
            VALUES (?, ?, ?)
        """,
            (word, ip_address, user_agent),
        )
        conn.commit()


def get_today_query_count(DATABASE_FILE):
    with closing(sqlite3.connect(DATABASE_FILE)) as conn:
        c = conn.cursor()
        c.execute(
            """
            SELECT COUNT(*) FROM query_log
            WHERE DATE(timestamp) = DATE('now')
        """
        )
        return c.fetchone()[0]
