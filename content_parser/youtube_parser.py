import os
import requests

from dotenv import load_dotenv 
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


def youtube_video_id_parser(YOUTUBE_API_KEY: str,
                            query: str,
                            max_results: int) -> list[str]:
    """Функция парсит выдачу Youtube по запросу
    query и возвращает список ID видео из первых max_results результатов"""
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
    Парсит субтитры c youtube на указанном языке.
    :param video_id: ID видео на YouTube.
    :param language_code: Язык субтитров, по умолчанию "en".
    :return: Субтитры на указанном языке или None, если их нет.
    """
    try:
        # Получаем список доступных субтитров для видео
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # Пробуем получить субтитры на указанном языке
        if language_code in transcript_list._manually_created_transcripts:
            transcript = transcript_list.find_manually_created_transcript([language_code])
        else:
            transcript = transcript_list.find_generated_transcript([language_code])
        # Форматируем субтитры как текст
        formatter = TextFormatter()
        subtitles_text = formatter.format_transcript(transcript.fetch())
        return subtitles_text
    except Exception as e:
        print(f"Ошибка при извлечении субтитров: {e}")
        return None


def split_text(text, chunk_size):
    """Разделяет текст на части указанного размера"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def text_translator_mymemory(text: str, src='en', dest='ru') -> str:
    """Переводит полученный текст с языка src, на язык dest, используя 
    бесплатный API MyMemory"""

    # URL для MyMemory API
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
            translated_chunk= json_response['responseData']['translatedText']
            translated_text.append(translated_chunk)
        else:
            print(f"Ошибка перевода части текста: {response.status_code}")
            break
    return translated_text
    
    print("Переведённые субтитры:", translated_text)
    return ' '.join(translated_text)


def main():
    load_dotenv()
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    query = 'top 5 anime in the world'
    max_results = 5
    #res = youtube_video_id_parser(YOUTUBE_API_KEY, query, max_results)
    #print(res)
    subtitles = ""
    for i in range(5):
        #    subtitles = youtube_subtitles_parser(res[i])
        if subtitles:
            print("===================================================")
            res = text_translator_mymemory(subtitles)
            print(res)
            break
        print("===================================================")
    test2 = youtube_subtitles_parser('Yd95LBhuSOk', 'ru')
    if test2:
        print("=================оригинал ютуб====================")
        print(test2)
        print("=================оригинал ютуб====================")
    else:
        print("*******************перевод***************")
        test2 = youtube_subtitles_parser('Yd95LBhuSOk', 'en')
        print(text_translator_mymemory(test2))
        print("*******************перевод***************")


if __name__ == '__main__':
    main()
