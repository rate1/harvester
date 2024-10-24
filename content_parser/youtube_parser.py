import os
import time
import random
import logging
import requests

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter


logger = logging.getLogger(__name__)


def youtube_video_id_parser(YOUTUBE_API_KEY: str,
                            query: str,
                            max_results: int,
                            retries=3,
                            backoff_time=2) -> list[str]:
    """
    Парсит выдачу YouTube по запросу.
    Парсит выдачу YouTube по запросу query и возвращает список результатов в
    количестве max_results штук.
    Args:
        YOUTUBE_API_KEY(str): API ключ YouTube.
        query(str): Поисковый запрос.
        max_results(int): Максимальное количество получаемых результатов.
        retries(int): Количество повторных попыток в случае неудачи.
        backoff_time(int): Время задержки перед повторной попыткой (в секундах).
    Returns:
        list[str]: Список id видео из первых результатов поиска в количестве
                    max_results штук.
    Raises:
    """
    if not YOUTUBE_API_KEY:
        logger.error("API ключ для YouTube не может быть пустым.")
        return []

    if max_results <=0:
        logger.error("max_results должно быть больше нуля.")
        return []

    url_youtube_data_api = (f"https://www.googleapis.com/youtube/v3/search?"
                            f"part=snippet&"
                            f"maxResults={max_results}&"
                            f"q={query}&"
                            f"type=video&"
                            f"videoDuration=long&"
                            f"key={YOUTUBE_API_KEY}")

    list_of_id = []

    for attempt in range(retries):
        try:
            response = requests.get(url_youtube_data_api)

            if response.status_code == 200:
                data = response.json()

                for item in data.get('items', []):
                    video_id = item['id'].get('videoId')
                    title = item['snippet'].get('title')

                    if video_id and title:
                        list_of_id.append(video_id)
                        logger.info(f"ID: {video_id}, Title: {title}")
                    else:
                        logger.warning("Недостаточные данные для одного из видео")
                logger.info(f"Получено {len(list_of_id)} id по запросу '{query}' на YouTube")
                return list_of_id

            else:
                logger.error(f"Ошибка запроса к API YouTube: {response.status_code}")
                break
        except requests.exceptions.Timeout:
            logger.warning(f"Превышено время ожидания. Попытка {attempt+1} из {retries}.")
            time.sleep(backoff_time)
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе: {e}")
            break

    return list_of_id


def youtube_subtitles_parser(video_id: str, language_code="en",
                             retries=3, backoff_time=2) -> str:
    """
    Парсит субтитры c YouTube на указанном языке.
    Args:
        video_id(str): ID видео на YouTube.
        language_code(str): Язык субтитров, по умолчанию "en".
        retries(int): Количество повторных попыток в случае неудачи.
        backoff_time(int): Время задержки перед повторной попыткой (в секундах).
    Returns:
        str: Субтитры на указанном языке или None, если их нет.
    """
    if not video_id:
        logger.error("video_id не может быть пустым.")
        return None

    for attempt in range(retries):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            if language_code in transcript_list._manually_created_transcripts:
                transcript = transcript_list.find_manually_created_transcript([language_code])
                logger.info(f"Получены вручную созданные субтитры на языке {language_code}.")
            else:
                transcript = transcript_list.find_generated_transcript([language_code])
                logger.info(f"Получены сгенерированные субтитры на языке {language_code}.")
            formatter = TextFormatter()
            subtitles_text = formatter.format_transcript(transcript.fetch())
            return subtitles_text

        except NoTranscriptFound:
            logger.error(f"Субтитры на языке '{language_code}' не найдены для видео ID {video_id}.")
            return None

        except TranscriptsDisabled:
            logger.error(f"Субтитры отключены для видео ID {video_id}.")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети при попытке получить субтитры: {e}")
            if attempt < retries - 1:
                logger.info(f"Попытка {attempt + 1} из {retries}, повтор через {backoff_time} секунд.")
                time.sleep(backoff_time)
            else:
                logger.error("Превышено количество попыток, не удалось получить субтитры.")
                return None

        except Exception as e:
            logger.error(f"Непредвиденная ошибка при извлечении субтитров: {e}")
            return None


def main():
    load_dotenv()
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    query = input("Введите запрос для поиска видео на ютуб: ")
    max_results = 5
    res = youtube_video_id_parser(YOUTUBE_API_KEY, query, max_results)
    print(res)
    subtitles = ""
    subtitles = youtube_subtitles_parser(res[0], 'ru')
    if subtitles:
        print("Оригинальные субтитры YouTube на русском языке:")
        print(subtitles)
    else:
        print("Переведенные субтитры YouTube на русском языке:")
        subtitles = youtube_subtitles_parser(res[0], 'en')
        print(text_translator_mymemory(subtitles))


if __name__ == '__main__':
    main()
