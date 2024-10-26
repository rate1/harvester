import sqlite3
import logging
from contextlib import closing


logger = logging.getLogger(__name__)


def initialize_db(db_name="harvester_data.db") -> None:
    """
    Создает базу данных sqlite с указанным именем.
    Args:
        db_name(str): Имя файла базы данных, по умолчанию 'harvester_data.db'.
    """
    with closing(sqlite3.connect(db_name)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    video_id TEXT PRIMARY KEY,
                    title TEXT,
                    subtitles TEXT,
                    rewritten_subtitles TEXT
                )
            """)

# Функции для записи данных
def save_video_data(video_id, title, db_name="project_data.db"):
    with closing(sqlite3.connect(db_name)) as conn:
        with conn:
            conn.execute("""
                INSERT OR IGNORE INTO videos (video_id, title)
                VALUES (?, ?)
            """, (video_id, title))

def save_subtitles(video_id, subtitles, db_name="project_data.db"):
    with closing(sqlite3.connect(db_name)) as conn:
        with conn:
            conn.execute("""
                UPDATE videos SET subtitles = ?
                WHERE video_id = ?
            """, (subtitles, video_id))

def save_rewrite(video_id, rewritten_subtitles, db_name="project_data.db"):
    with closing(sqlite3.connect(db_name)) as conn:
        with conn:
            conn.execute("""
                UPDATE videos SET rewritten_subtitles = ?
                WHERE video_id = ?
            """, (rewritten_subtitles, video_id))import
