from typing import NamedTuple


class Language(NamedTuple):
    code: str
    table_name: str = "languages"

class Translator(NamedTuple):
    translator: str
    table_name: str = "translators"

class Publication_status(NamedTuple):
    status: str
    table_name: str = "publication_status"

class Subject(NamedTuple):
    subject: str
    table_name: str = "subjects"

class Category(NamedTuple):
    category: str
    subject_id: int
    table_name: str = "categories"

class Topic(NamedTuple):
    topic: str
    category_id: int
    table_name: str = "topics"

class Platform(NamedTuple):
    name: str
    url: str
    table_name: str = "platforms"

class Channel(NamedTuple):
    name: str
    url: str
    platform_id: int
    subject_id: int
    table_name: str = "channels"

class Channel_category(NamedTuple):
    channel_id: int
    category_id: int
    table_name: str = "channels_categories"

class Original_text(NamedTuple):
    language_id: int
    text: str
    topic_id: int
    created_at: str
    updated_at: str
    table_name: str = "original_texts"

class Video(NamedTuple):
    youtube_id: str
    title: str
    description: str
    topic_id: int
    text_id: int
    created_at: str
    updated_at: str
    table_name: str = "videos"

class Translate(NamedTuple):
    text_id: int 
    language_id: int
    translated_text: str
    translator_id: int
    created_at: str
    updated_at: str
    table_name: str = "translates"

class Rewrite(NamedTuple):
    rewrite_text: str
    language_id: int
    translate_id: int
    topic_id: int
    created_at: str
    updated_at: str
    table_name: str = "rewrites"

class Publication(NamedTuple):
    rewrite_id: int 
    channel_id: int
    publish_date: str
    status_id: int
    published_url: str
    created_at: str
    updated_at: str
    table_name: str = "publications"
