import sqlite3
from pathlib import Path
from typing import Optional


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self):
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS model_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    model_name TEXT NOT NULL,
                    response_text TEXT NOT NULL,
                    usage_info TEXT,
                    response_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(query_id) REFERENCES queries(id) ON DELETE CASCADE
                );
                CREATE INDEX IF NOT EXISTS idx_model_responses_query_model
                    ON model_responses(query_id, model_name);

                CREATE TABLE IF NOT EXISTS divergences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    diff_summary TEXT NOT NULL,
                    diff_detail TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(query_id) REFERENCES queries(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS structures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    structured_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(query_id) REFERENCES queries(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS fused_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    answer_text TEXT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(query_id) REFERENCES queries(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    diff_id TEXT NOT NULL,
                    evidence_text TEXT,
                    source TEXT,
                    verdict TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(query_id) REFERENCES queries(id) ON DELETE CASCADE
                );
                """
            )

    def save_query(self, question_text: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO queries(question_text) VALUES(?)",
                (question_text,),
            )
            return int(cur.lastrowid)

    def get_cached_response(self, question_text: str, model_name: str) -> Optional[str]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT mr.response_text
                FROM model_responses mr
                JOIN queries q ON q.id = mr.query_id
                WHERE q.question_text = ? AND mr.model_name = ?
                ORDER BY mr.id DESC
                LIMIT 1
                """,
                (question_text, model_name),
            ).fetchone()
            return row[0] if row else None

    def save_response(self, query_id: int, model_name: str, response_text: str, usage_info: str = ""):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO model_responses(query_id, model_name, response_text, usage_info)
                VALUES (?, ?, ?, ?)
                """,
                (query_id, model_name, response_text, usage_info),
            )

    def save_divergence(self, query_id: int, diff_summary: str, diff_detail: str):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO divergences(query_id, diff_summary, diff_detail)
                VALUES (?, ?, ?)
                """,
                (query_id, diff_summary, diff_detail),
            )

    def save_structure(self, query_id: int, structured_data: str):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO structures(query_id, structured_data)
                VALUES (?, ?)
                """,
                (query_id, structured_data),
            )

    def save_fused_answer(self, query_id: int, answer_text: str, notes: str = ""):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO fused_answers(query_id, answer_text, notes)
                VALUES (?, ?, ?)
                """,
                (query_id, answer_text, notes),
            )

    def save_evidence(self, query_id: int, diff_id: str, evidence_text: str, source: str, verdict: str):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO evidence(query_id, diff_id, evidence_text, source, verdict)
                VALUES (?, ?, ?, ?, ?)
                """,
                (query_id, diff_id, evidence_text, source, verdict),
            )

