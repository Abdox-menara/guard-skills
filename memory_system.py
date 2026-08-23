"""
SQLite Memory System for Tracking User Preferences and Task History.

This module provides a robust, thread-safe SQLite-based storage system for
managing user preferences and logging task execution history.
"""

import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from contextlib import contextmanager
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SQLiteMemorySystem:
    """A production-ready SQLite memory system for tracking user preferences
    and task history with thread safety and error handling."""

    def __init__(self, db_path: str = "memory_system.db"):
        self.db_path = Path(db_path)
        self._lock = threading.RLock()
        self._ensure_db_directory()

    def _ensure_db_directory(self) -> None:
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _get_connection(self) -> sqlite3.Connection:
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path,
                timeout=30.0,
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def init_db(self) -> None:
        with self._lock:
            with self._get_connection() as conn:
                try:
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS preferences (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT NOT NULL,
                            preference_key TEXT NOT NULL,
                            preference_value TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE(user_id, preference_key)
                        )
                    """)
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS task_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT NOT NULL,
                            task_name TEXT NOT NULL,
                            task_status TEXT NOT NULL,
                            task_data TEXT,
                            started_at TIMESTAMP NOT NULL,
                            completed_at TIMESTAMP,
                            duration_seconds REAL,
                            error_message TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_preferences_user_id ON preferences(user_id)")
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_task_history_user_id ON task_history(user_id)")
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_task_history_task_name ON task_history(task_name)")
                    conn.execute("CREATE INDEX IF NOT EXISTS idx_task_history_status ON task_history(task_status)")
                    conn.commit()
                    logger.info("Database initialized successfully")
                except sqlite3.Error as e:
                    logger.error(f"Failed to initialize database: {e}")
                    raise

    def set_preference(self, user_id: str, key: str, value: Union[str, int, float, bool, Dict, List]) -> None:
        if not user_id or not key:
            raise ValueError("user_id and key must not be empty")

        if isinstance(value, (dict, list, bool, int, float)):
            value_str = json.dumps(value)
        else:
            value_str = str(value)

        with self._lock:
            with self._get_connection() as conn:
                try:
                    conn.execute("""
                        INSERT INTO preferences (user_id, preference_key, preference_value, updated_at)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(user_id, preference_key) DO UPDATE SET
                        preference_value = excluded.preference_value,
                        updated_at = CURRENT_TIMESTAMP
                    """, (user_id, key, value_str))
                    conn.commit()
                    logger.debug(f"Set preference: user_id={user_id}, key={key}")
                except sqlite3.Error as e:
                    logger.error(f"Failed to set preference: {e}")
                    raise

    def get_preference(self, user_id: str, key: str, default: Any = None) -> Any:
        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.execute("""
                        SELECT preference_value FROM preferences
                        WHERE user_id = ? AND preference_key = ?
                    """, (user_id, key))
                    row = cursor.fetchone()
                    if row is None:
                        return default
                    value_str = row["preference_value"]
                    try:
                        return json.loads(value_str)
                    except (json.JSONDecodeError, TypeError):
                        return value_str
                except sqlite3.Error as e:
                    logger.error(f"Failed to get preference: {e}")
                    raise

    def get_all_preferences(self, user_id: str) -> Dict[str, Any]:
        preferences: Dict[str, Any] = {}
        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.execute("""
                        SELECT preference_key, preference_value FROM preferences
                        WHERE user_id = ?
                        ORDER BY preference_key
                    """, (user_id,))
                    for row in cursor.fetchall():
                        key = row["preference_key"]
                        value_str = row["preference_value"]
                        try:
                            preferences[key] = json.loads(value_str)
                        except (json.JSONDecodeError, TypeError):
                            preferences[key] = value_str
                    logger.debug(f"Retrieved {len(preferences)} preferences for user_id={user_id}")
                    return preferences
                except sqlite3.Error as e:
                    logger.error(f"Failed to get all preferences: {e}")
                    raise

    def delete_preference(self, user_id: str, key: str) -> bool:
        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.execute("""
                        DELETE FROM preferences
                        WHERE user_id = ? AND preference_key = ?
                    """, (user_id, key))
                    conn.commit()
                    return cursor.rowcount > 0
                except sqlite3.Error as e:
                    logger.error(f"Failed to delete preference: {e}")
                    raise

    def log_task(
        self,
        user_id: str,
        task_name: str,
        status: str,
        task_data: Optional[Union[Dict, List, str]] = None,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        error_message: Optional[str] = None
    ) -> int:
        if not user_id or not task_name or not status:
            raise ValueError("user_id, task_name, and status must not be empty")

        task_data_str = json.dumps(task_data) if task_data else None
        started_at_str = (started_at or datetime.now()).isoformat()
        completed_at_str = completed_at.isoformat() if completed_at else None
        duration = (completed_at - started_at).total_seconds() if completed_at and started_at else None

        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.execute("""
                        INSERT INTO task_history
                        (user_id, task_name, task_status, task_data, started_at, completed_at, duration_seconds, error_message)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, task_name, status, task_data_str, started_at_str, completed_at_str, duration, error_message))
                    conn.commit()
                    task_id = cursor.lastrowid
                    logger.debug(f"Logged task: id={task_id}, name={task_name}, status={status}")
                    return task_id
                except sqlite3.Error as e:
                    logger.error(f"Failed to log task: {e}")
                    raise

    def get_recent_tasks(self, user_id: str, limit: int = 10, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            with self._get_connection() as conn:
                try:
                    query = "SELECT * FROM task_history WHERE user_id = ?"
                    params: list = [user_id]
                    if status_filter:
                        query += " AND task_status = ?"
                        params.append(status_filter)
                    query += " ORDER BY created_at DESC LIMIT ?"
                    params.append(limit)

                    cursor = conn.execute(query, params)
                    tasks = []
                    for row in cursor.fetchall():
                        task = dict(row)
                        if task.get("task_data"):
                            try:
                                task["task_data"] = json.loads(task["task_data"])
                            except (json.JSONDecodeError, TypeError):
                                pass
                        tasks.append(task)
                    return tasks
                except sqlite3.Error as e:
                    logger.error(f"Failed to get recent tasks: {e}")
                    raise

    def clear_old_tasks(self, user_id: str, days_to_keep: int = 30) -> int:
        with self._lock:
            with self._get_connection() as conn:
                try:
                    cursor = conn.execute("""
                        DELETE FROM task_history
                        WHERE user_id = ? AND created_at < datetime('now', ? || ' days')
                    """, (user_id, f"-{days_to_keep}"))
                    conn.commit()
                    deleted = cursor.rowcount
                    logger.info(f"Cleared {deleted} old tasks for user_id={user_id}")
                    return deleted
                except sqlite3.Error as e:
                    logger.error(f"Failed to clear old tasks: {e}")
                    raise


if __name__ == "__main__":
    db = SQLiteMemorySystem("opencode_memory.db")
    db.init_db()

    db.set_preference("default_user", "preferred_shell", "PowerShell")
    db.set_preference("default_user", "preferred_language", "Python")
    db.set_preference("default_user", "theme", {"dark": True, "font_size": 14})

    print("Preferences:", db.get_all_preferences("default_user"))

    db.log_task(
        user_id="default_user",
        task_name="system_cleanup",
        status="success",
        task_data={"files_deleted": 150, "space_freed_mb": 500}
    )

    print("Recent tasks:", db.get_recent_tasks("default_user", limit=5))
