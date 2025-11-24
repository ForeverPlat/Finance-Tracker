# db.py
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Iterable, Dict, Any, Optional

DB_PATH = Path("tracking.db")


class TransactionDB:
    def __init__(self, db_path: Path | str = DB_PATH) -> None:
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total REAL NOT NULL,
                amount REAL NOT NULL,
                category TEXT,
                comment TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

        # initial zero row if table is empty
        cur.execute("SELECT COUNT(*) AS count FROM tracking")
        if cur.fetchone()["count"] == 0:
            self._insert_row(total=0.0, amount=0.0, category="", comment="Initial")

    def _insert_row(self, total: float, amount: float, category: str, comment: str):
        self.conn.execute(
            """
            INSERT INTO tracking (total, amount, category, comment)
            VALUES (?, ?, ?, ?)
            """,
            (total, amount, category, comment),
        )
        self.conn.commit()

    def get_current_total(self) -> float:
        cur = self.conn.cursor()
        cur.execute("SELECT total FROM tracking ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        return float(row["total"]) if row else 0.0

    def add_transaction(self, amount: float, category: str, comment: str) -> float:
        current_total = self.get_current_total()
        new_total = current_total + amount
        self._insert_row(new_total, amount, category, comment)
        return new_total

    def get_all(self) -> Iterable[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tracking ORDER BY id DESC")
        for row in cur.fetchall():
            yield dict(row)

    def close(self):
        self.conn.close()
