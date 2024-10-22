import logging

from dotenv import load_dotenv
from content_parser.youtube_parser import youtube_subtitles_parser
from content_parser.youtube_parser import text_translator_mymemory
from rewrite.chatgpt_rewrite import gpt_rewrite


logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
)


def main():
    load_dotenv()
    youtube_id = input("Введите id ролика на YouTube: ")
    try:
        logging.info(f"Получаем субтитры для ролика с ID: {youtube_id}")
        subtitles = youtube_subtitles_parser(youtube_id, 'ru')
        if subtitles:
            logging.info("Оригинальные русские субтитры получены.")
        else:
            logging.info("Русских субтитров нет, пробую получить английские.")
            en_subtitles = youtube_subtitles_parser(youtube_id, 'en')
            if en_subtitles:
                subtitles = text_translator_mymemory(en_subtitles)
                logging.info("Английские субтитры переведены.")
            else:
                logging.error("Английских субтитров нет. Прерывание процесса.")
                return
    except Exception as e:
        logging.error(f"Ошибка при получении или переводе субтитров: {e}")
        return

    try:
        logging.info("Начинается рерайт текста.")
        print(subtitles)
        article_text = gpt_rewrite(subtitles)
        logging.info("Рерайт завершен успешно.")
        print("Текст статьи после рерайта:")
        print(article_text)
    except Exception as e:
        logging.error(f"Ошибка при рерайте текста: {e}")
        return


if __name__ == '__main__':
    main()
