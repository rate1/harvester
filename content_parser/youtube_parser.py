import os
import requests

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


def youtube_video_id_parser(YOUTUBE_API_KEY: str,
                            query: str,
                            max_results: int) -> list[str]:
    """
    Парсит выдачу YouTube по запросу.
    Парсит выдачу YouTube по запросу query и возвращает список результатов в
    количестве max_results штук.
    Args:
        YOUTUBE_API_KEY(str): API ключ YouTube.
        query(str): Поисковый запрос.
        max_results(int): Максимальное количество получаемых результатов.
    Returns:
        list[str]: Список id видео из первых результатов поиска в количестве
                    max_results штук.
    Raises:
    """
    url_youtube_data_api = (f"https://www.googleapis.com/youtube/v3/search?"
                            f"part=snippet&"
                            f"maxResults={max_results}&"
                            f"q={query}&"
                            f"type=video&"
                            f"videoDuration=long&"
                            f"key={YOUTUBE_API_KEY}")

    response = requests.get(url_youtube_data_api)
    list_of_id = []
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            list_of_id.append(video_id)
            print(f"Video ID: {video_id}, Title: {title}")
    else:
        print("Ошибка при выполнении запроса:", response.status_code)
    return list_of_id


def youtube_subtitles_parser(video_id: str, language_code="en") -> str:
    """
    Парсит субтитры c YouTube на указанном языке.
    Args:
        video_id(str): ID видео на YouTube.
        language_code(str): Язык субтитров, по умолчанию "en".
    Returns:
        str: Субтитры на указанном языке или None, если их нет.
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        if language_code in transcript_list._manually_created_transcripts:
            transcript = transcript_list.find_manually_created_transcript([language_code])
        else:
            transcript = transcript_list.find_generated_transcript([language_code])
        formatter = TextFormatter()
        subtitles_text = formatter.format_transcript(transcript.fetch())
        return subtitles_text
    except Exception as e:
        print(f"Ошибка при извлечении субтитров: {e}")
        return None


def split_text(text: str, chunk_size: int) -> list[str]:
    """
    Разделяет текст на части указанного размера.
    Args:
        text(str): Текст для разбивания на части.
        chunk_size(int): Размер получаемых частей.
    Returns:
        list[str]: Список, содержащий части поделенного текста.
    Raises:
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def text_translator_mymemory(text: str, src='en', dest='ru') -> str:
    """
    Переводит текст.
    Переводит полученный текст с языка src, на язык dest, используя
    бесплатный API MyMemory.
    Args:
        text(str): Текст для перевода.
        src(str): Язык оригинального текста для перевода.
        dest(str): Язык, на который необходимо произвести перевод.
    Returns:
        str: Переведенный текст.
    Raises:
    """
    url = "https://api.mymemory.translated.net/get"
    translated_text = []
    chunks = split_text(text, 500)
    for chunk in chunks:
        params = {
            'q': chunk,
            'langpair': f'{src}|{dest}'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            json_response = response.json()
            translated_chunk = json_response['responseData']['translatedText']
            translated_text.append(translated_chunk)
        else:
            print(f"Ошибка перевода части текста: {response.status_code}")
            break
    print("Переведённые субтитры:", translated_text)
    return ' '.join(translated_text)


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
