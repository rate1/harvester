import sqlite3
import logging

from typing import Optional


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
            
            # Таблица languages содержит возможные коды языков ("ru", "en"...).
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS languages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL
                );
                """)

            # Таблица translators содержит список доступных переводчиков.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    translator TEXT UNIQUE NOT NULL
                );
                """)

            # Таблица publication_status содержит статусы публикаций.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS publication_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT UNIQUE NOT NULL
                );
                """)

            # Таблица subjects содержит тематики ресурсов.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT UNIQUE NOT NULL
                );
                """)

            # Таблица categories содержит список категорий для разных тематик.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    subject_id INTEGER,
                    FOREIGN KEY (subject_id) REFERENCES subjects(id)
                );
                """)

            # Таблица topics содержит темы постов.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                );
                """)

            # Таблица platforms содержит платформы для размещения постов.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS platforms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    url TEXT UNIQUE NOT NULL
                );
                """)

            # Таблица channels содержит список каналов для публикации постов.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    platform_id INTEGER,
                    subject_id INTEGER,
                    FOREIGN KEY (platform_id) REFERENCES platforms(id),
                    FOREIGN KEY (subject_id) REFERENCES subjects(id)
                );
                """)

            # Таблица channels_categories содержит категории для каналов.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS channels_categories (
                    channel_id INTEGER,
                    category_id INTEGER,
                    PRIMARY KEY (channel_id, category_id),
                    FOREIGN KEY (channel_id) REFERENCES channels(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                );
                """)

            # Таблица original_texts содержит оригинальные тексты с источников.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS original_texts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    language_id INTEGER,
                    text TEXT,
                    topic_id INTEGER,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (topic_id) REFERENCES topics(id),
                    FOREIGN KEY (language_id) REFERENCES languages(id)
                );
                """)
            
            # Таблица videos содержит видео на YouTube для разных тематик.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    youtube_id TEXT UNIQUE NOT NULL,
                    title TEXT,
                    description TEXT,
                    topic_id INTEGER,
                    text_id INTEGER,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (topic_id) REFERENCES topics(id),
                    FOREIGN KEY (text_id) REFERENCES original_texts(id)
                );
                """)
            
            # Таблица translates содержит переводы текстов.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text_id INTEGER,
                    language_id INTEGER,
                    translated_text TEXT,
                    translator_id INTEGER,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (text_id) REFERENCES original_texts(id),
                    FOREIGN KEY (translator_id) REFERENCES translators(id),
                    FOREIGN KEY (language_id) REFERENCES languages(id)
                );
                """)

            # Таблица rewrites содержит рерайты переводов текстов.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rewrites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rewrite_text TEXT,
                    language_id INTEGER,
                    translate_id INTEGER,
                    topic_id INTEGER,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (translate_id) REFERENCES translates(id),
                    FOREIGN KEY (topic_id) REFERENCES topics(id),
                    FOREIGN KEY (language_id) REFERENCES languages(id)
                );
                """)
            
            # Таблица publications содержит список публикаций на каналах.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS publications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rewrite_id INTEGER,
                    channel_id INTEGER,
                    publish_date TEXT,
                    status_id INTEGER,
                    published_url TEXT,
                    FOREIGN KEY (rewrite_id) REFERENCES rewrites(id),
                    FOREIGN KEY (channel_id) REFERENCES channels(id),
                    FOREIGN KEY (status_id) REFERENCES publication_status(id),
                    CONSTRAINT unique_rewrite_channel UNIQUE (rewrite_id, channel_id)
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

def insert_subtitle(video_id: int, language_code: str, subtitle_text: str,
                    db_name="content_harvester.db") -> Optional[int]:
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
    

def main():
    initialize_db()


if __name__ == '__main__':
    main()
