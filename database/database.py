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

