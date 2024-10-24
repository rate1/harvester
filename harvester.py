import logging

from dotenv import load_dotenv
from content_parser.youtube_parser import youtube_subtitles_parser
from translate.translate import text_translator_mymemory, text_translator_yandex
from rewrite.chatgpt_rewrite import gpt_rewrite


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
    youtube_id = input("Введите id ролика на YouTube: ")
    try:
        logger.info(f"Получаем субтитры для ролика с ID: {youtube_id}")
        subtitles = youtube_subtitles_parser(youtube_id, 'ru')
        if subtitles:
            logger.info("Оригинальные русские субтитры получены.")
        else:
            logger.info("Русских субтитров нет, пробую получить английские.")
            en_subtitles = youtube_subtitles_parser(youtube_id, 'en')
            if en_subtitles:
                subtitles = text_translator_yandex(en_subtitles)
                print(subtitles)
                logger.info("Английские субтитры переведены.")
            else:
                logger.error("Английских субтитров нет. Прерывание процесса.")
                return
    except Exception as e:
        logger.error(f"Ошибка при получении или переводе субтитров: {e}")
        return

    try:
        if subtitles:
            logger.info("Начинается рерайт текста.")
            article_text = gpt_rewrite(subtitles)
            logger.info("Рерайт завершен успешно.")
            print("Текст статьи после рерайта:")
            print(article_text)
        else:
            logger.info("Текст для рерайта не был получен.")
    except Exception as e:
        logger.error(f"Ошибка при рерайте текста: {e}")
        return


if __name__ == '__main__':
    main()
