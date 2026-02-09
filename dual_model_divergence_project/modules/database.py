import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA busy_timeout = 5000")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _has_column(conn: sqlite3.Connection, table: str, column: str) -> bool:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
        names = {r[1] for r in rows}
        return column in names

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
                    source_tier TEXT,
                    auto_applied INTEGER DEFAULT 0,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(query_id) REFERENCES queries(id) ON DELETE CASCADE
                );
                """
            )
            # Lightweight migration path for existing databases.
            if not self._has_column(conn, "evidence", "source_tier"):
                conn.execute("ALTER TABLE evidence ADD COLUMN source_tier TEXT")
            if not self._has_column(conn, "evidence", "auto_applied"):
                conn.execute("ALTER TABLE evidence ADD COLUMN auto_applied INTEGER DEFAULT 0")
            if not self._has_column(conn, "evidence", "confidence"):
                conn.execute("ALTER TABLE evidence ADD COLUMN confidence REAL")

    def save_query(self, question_text: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO queries(question_text) VALUES(?)",
                (question_text,),
            )
            return int(cur.lastrowid)

    def get_cached_response(
        self,
        question_text: str,
        model_name: str,
        response_mode: Optional[str] = None,
    ) -> Optional[str]:
        with self._connect() as conn:
            if response_mode:
                row = conn.execute(
                    """
                    SELECT mr.response_text
                    FROM model_responses mr
                    JOIN queries q ON q.id = mr.query_id
                    WHERE q.question_text = ?
                      AND mr.model_name = ?
                      AND mr.usage_info LIKE ?
                    ORDER BY mr.id DESC
                    LIMIT 1
                    """,
                    (question_text, model_name, f"mode={response_mode}%"),
                ).fetchone()
            else:
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

    def save_evidence(
        self,
        query_id: int,
        diff_id: str,
        evidence_text: str,
        source: str,
        verdict: str,
        source_tier: str = "",
        auto_applied: int = 0,
        confidence: float = 0.0,
    ):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO evidence(
                    query_id, diff_id, evidence_text, source, verdict, source_tier, auto_applied, confidence
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (query_id, diff_id, evidence_text, source, verdict, source_tier, auto_applied, confidence),
            )
