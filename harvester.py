from dotenv import load_dotenv
from content_parser.youtube_parser import youtube_subtitles_parser
from content_parser.youtube_parser import text_translator_mymemory
from rewrite.chatgpt_rewrite import gpt_rewrite


def main():
    load_dotenv()
    subtitles = youtube_subtitles_parser('Yd95LBhuSOk', 'ru')
    if subtitles:
        print("Получены оригинальные субтитры с youtube")
    else:
        en_subtitles = youtube_subtitles_parser('Yd95LBhuSOk', 'en')
        subtitles = text_translator_mymemory(en_subtitles)
        print("Получены английские субтитры с youtube и переведены")
    print(subtitles)

    article_text = gpt_rewrite(subtitles)
    print("Текст статьи после рерайта:")
    print(article_text)


if __name__ == '__main__':
    main()
