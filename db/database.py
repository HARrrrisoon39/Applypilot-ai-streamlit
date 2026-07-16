import sqlite3
from config import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title         TEXT NOT NULL,
                company           TEXT NOT NULL,
                job_url           TEXT,
                deadline          TEXT,
                status            TEXT DEFAULT 'applied',
                skills_analysis   TEXT,
                cover_letter      TEXT,
                interview_questions TEXT,
                created_at        TEXT DEFAULT (datetime('now'))
            )
        """)
        # Migrate existing tables that lack the new columns
        existing = {row[1] for row in conn.execute("PRAGMA table_info(applications)").fetchall()}
        for col, definition in [
            ("skills_analysis", "TEXT"),
            ("interview_questions", "TEXT"),
        ]:
            if col not in existing:
                conn.execute(f"ALTER TABLE applications ADD COLUMN {col} {definition}")
        conn.commit()


def save_application(data: dict) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """INSERT INTO applications
               (job_title, company, job_url, deadline, status, skills_analysis, cover_letter, interview_questions)
               VALUES (:job_title, :company, :job_url, :deadline, :status,
                       :skills_analysis, :cover_letter, :interview_questions)""",
            {
                "job_title": data["job_title"],
                "company": data["company"],
                "job_url": data.get("job_url", ""),
                "deadline": data.get("deadline", ""),
                "status": data.get("status", "applied"),
                "skills_analysis": data.get("skills_analysis", ""),
                "cover_letter": data.get("cover_letter", ""),
                "interview_questions": data.get("interview_questions", ""),
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
