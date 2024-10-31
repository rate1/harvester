import sqlite3
import logging


logger = logging.getLogger(__name__)


def initialize_db(db_name="harvester_data.db") -> None:
    """
    Создает базу данных sqlite с указанным именем.
    Args:
        db_name(str): Имя файла базы данных, по умолчанию 'harvester_data.db'.
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    platform TEXT NOT NULL
                );
                """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    youtube_id TEXT UNIQUE NOT NULL,
                    title TEXT,
                    description TEXT,
                    channel_id INTEGER,
                    FOREIGN KEY (channel_id) REFERENCES channels(id)
                );
                """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subtitles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER,
                    language_code TEXT,
                    original_text TEXT,
                    translated_text TEXT,
                    FOREIGN KEY (video_id) REFERENCES videos(id)
                );
                """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rewrites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subtitle_id INTEGER,
                    rewrite_text TEXT,
                    FOREIGN KEY (subtitle_id) REFERENCES subtitles(id)
                );
                """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS publications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rewrite_id INTEGER,
                    channel_id INTEGER,
                    publish_date TEXT,
                    status TEXT,
                    published_url TEXT,
                    FOREIGN KEY (rewrite_id) REFERENCES rewrites(id),
                    FOREIGN KEY (channel_id) REFERENCES channels(id)
                );
                """)
            
            conn.commit()
            logger.info(f"База данных {db_name} успешно инициализирована.")
            
    except sqlite3.Error as e:
        logger.error(f"Ошибка инициализации базы данных: {e}")


def insert_channel(name: str, platform: str, db_name="content_harvester.db") -> Optional[int]:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO channels (name, platform) VALUES (?, ?)", (name, platform))
        conn.commit()
        return cursor.lastrowid

def insert_video(youtube_id: str, title: str, description: str, upload_date: str, channel_id: int, db_name="content_harvester.db") -> Optional[int]:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO videos (youtube_id, title, description, upload_date, channel_id) VALUES (?, ?, ?, ?, ?)",
            (youtube_id, title, description, upload_date, channel_id)
        )
        conn.commit()
        return cursor.lastrowid

def insert_subtitle(video_id: int, language_code: str, subtitle_text: str, db_name="content_harvester.db") -> Optional[int]:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO subtitles (video_id, language_code, subtitle_text) VALUES (?, ?, ?)",
            (video_id, language_code, subtitle_text)
        )
        conn.commit()
        return cursor.lastrowid

def insert_rewrite(subtitle_id: int, rewrite_text: str, db_name="content_harvester.db") -> Optional[int]:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rewrites (subtitle_id, rewrite_text) VALUES (?, ?)",
            (subtitle_id, rewrite_text)
        )
        conn.commit()
        return cursor.lastrowid

def insert_publication(rewrite_id: int, channel_id: int, publish_date: str, status: str, published_url: str, db_name="content_harvester.db") -> Optional[int]:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO publications (rewrite_id, channel_id, publish_date, status, published_url) VALUES (?, ?, ?, ?, ?)",
            (rewrite_id, channel_id, publish_date, status, published_url)
        )
        conn.commit()
        return cursor.lastrowid
