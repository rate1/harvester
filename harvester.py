import logging

from dotenv import load_dotenv
from content_parser.youtube_parser import youtube_subtitles_parser
from translate.translate import text_translator_mymemory, text_translator_yandex
from rewrite.chatgpt_rewrite import gpt_rewrite
from prompts import PROMPT_REWRITE


logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    youtube_id = input("Введите ID ролика на YouTube: ")
    try:
        logger.info(f"Получаем субтитры для ролика с ID: {youtube_id}")
        subtitles = youtube_subtitles_parser(youtube_id, 'ru')
        if subtitles:
            logger.info(f"Оригинальные русские субтитры получены. Длина текста: {len(subtitles)}.")
        else:
            logger.info("Русских субтитров нет, пробую получить английские.")
            en_subtitles = youtube_subtitles_parser(youtube_id, 'en')
            if en_subtitles:
                subtitles = text_translator_yandex(en_subtitles)
                logger.info(f"Английские субтитры переведены. Длина текста: {len(subtitles)}.")
            else:
                logger.error("Английских субтитров нет. Прерывание процесса.")
                return
    except Exception as e:
        logger.error(f"Ошибка при получении или переводе субтитров: {e}")
        return

    try:
        if subtitles:
            logger.info("Начинается рерайт текста.")
            article_text = gpt_rewrite(subtitles, PROMPT_REWRITE, max_tokens=6000)
            logger.info(f"Рерайт завершен успешно. Длина текста: {len(article_text)}.")
            print("Текст статьи после рерайта:")
            print(article_text)
        else:
            logger.info("Текст для рерайта не был получен.")
    except Exception as e:
        logger.error(f"Ошибка при рерайте текста: {e}")
        return


if __name__ == '__main__':
    main()
