import sqlite3
from config import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title   TEXT,
                company     TEXT,
                job_url     TEXT,
                deadline    TEXT,
                status      TEXT DEFAULT 'applied',
                cover_letter TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


def save_application(data: dict) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """INSERT INTO applications (job_title, company, job_url, deadline, status, cover_letter)
               VALUES (:job_title, :company, :job_url, :deadline, :status, :cover_letter)""",
            {
                "job_title": data.get("job_title", ""),
                "company": data.get("company", ""),
                "job_url": data.get("job_url", ""),
                "deadline": data.get("deadline", ""),
                "status": data.get("status", "applied"),
                "cover_letter": data.get("cover_letter", ""),
            },
        )
        conn.commit()
        return cur.lastrowid


def list_applications() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM applications ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def update_status(app_id: int, status: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE applications SET status = ? WHERE id = ?", (status, app_id)
        )
        conn.commit()


def delete_application(app_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()
