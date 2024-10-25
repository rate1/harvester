import os
import time
import random
import logging
import requests

from dotenv import load_dotenv
from utils.utils import split_text

logger = logging.getLogger(__name__)


def text_translator_yandex(text: str, src='en', dest='ru') -> str:
    """
    Переводит текст с использованием Yandex Translate API.
    Args:
        text (str): Текст для перевода.
        src (str): Язык исходного текста (например, 'en').
        dest (str): Язык перевода (например, 'ru').
    Returns:
        str: Переведённый текст или сообщение об ошибке.
    """
    YANDEX_API_URL = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    YANDEX_API_KEY = os.environ.get('YANDEX_API_KEY')

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }

    chanks = split_text(text, 8000)
    translated_text = []

    for chunk in chanks:
        try:
            body = {
                "sourceLanguageCode": src,
                "targetLanguageCode": dest,
                "texts": [chunk]
            }

            response = requests.post(YANDEX_API_URL, json=body, headers=headers)

            if response.status_code == 200:
                result = response.json()
                translated_chunk = result['translations'][0]['text']
                translated_text.append(translated_chunk)
                logger.info(f"Часть текста успешно переведена: {translated_chunk[:30]}...")
            else:
                logger.error(f"Ошибка перевода: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети при попытке перевода: {e}")
            return "Ошибка сети при переводе текста."

    return ' '.join(translated_text)


def text_translator_mymemory(text: str, src='en', dest='ru',
                             retries=3, backoff_time=2) -> str:
    """
    Переводит текст.
    Переводит полученный текст с языка src, на язык dest, используя
    бесплатный API MyMemory.
    Args:
        text(str): Текст для перевода.
        src(str): Язык оригинального текста для перевода.
        dest(str): Язык, на который необходимо произвести перевод.
        retries(int): Количество повторных попыток в случае неудачи.
        backoff_time(int): Начальное время задержки между попытками (в секундах).
    Returns:
        str: Переведенный текст.
    Raises:
    """
    url = "https://api.mymemory.translated.net/get"
    translated_text = []
    chunks = split_text(text, 500)
    for chunk in chunks:
        for attempt in range(retries):
            try:
                params = {
                    'q': chunk,
                    'langpair': f'{src}|{dest}'
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    json_response = response.json()
                    translated_chunk = json_response['responseData']['translatedText']
                    translated_text.append(translated_chunk)
                    logger.info(f"Успешно переведена часть текста: {translated_chunk[:30]}...")
                    time.sleep(1 + random.uniform(0, 1))
                    break
                else:
                    logger.error(f"Ошибка перевода части текста: {response.status_code}, попытка {attempt+1}.")
                    if attempt < retries - 1:
                        wait_time = backoff_time * (2 ** attempt) + random.uniform(0, 1)
                        logger.info(f"Повтор попытки через {wait_time:.2f} секунд.")
                        time.sleep(wait_time)
                    else:
                        logger.error("Превышено количество попыток. Перевод прерван.")
            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка сети при попытке перевода: {e}")
                if attempt < retries - 1:
                    wait_time = backoff_time * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Повтор попытки через {wait_time:.2f} секунд.")
                    time.sleep(wait_time)
                else:
                    logger.error("Превышено количество попыток. Перевод прерван.")

    return ' '.join(translated_text)


def main():
    load_dotenv()

if __name__ == '__main__':
    main()
