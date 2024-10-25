import os

from openai import OpenAI


def gpt_rewrite(text: str, temperature=0.7, max_tokens=1500) -> str:
    """
    Делает рерайт текста с помощью chatgpt.
    Args:
        text(str): Текст для рерайта.
        temperature(float): Значение в диапазоне [0;1], чем больше число, тем
        более креативным будет ответ. По умолчанию значение 0.7.
        max_tokens(int): Максимальное количество токенов chatgpt, по умолчанию
        1500 штук.
    Returns:
        str: Измененный с помощью рерайта текст.
    Raises:
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Или другой доступный движок GPT
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты David Ogilvy,занимаешься качественным "
                    "копирайтом текста. Профессионал своего дела.")
             },
            {
                 "role": "user",
                 "content": (
                    f"Переформулируй без потери контекста и объемности "
                    f"указанный после двоеточия текст "
                    f"и адаптируй его так, чтобы он идеально подходил "
                    f"для публикации в виде статьи на Яндекс.Дзен. "
                    f"Сохрани стилистические элементы, примеры в все пояснения "
                    f"Очеловечь этот текст и убери из него "
                    f"предложения лишенные смысла, оживи и создай "
                    f"сенсацию, чтобы текст вызывал желание дочитать "
                    f"статью до самого конца."
                    f"Из текста необходимо "
                    f"убрать прямую речь от имени рассказчика: "
                    f"\n\n{text}")
             }
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].message.content.strip().replace('.\n', '. ').replace('\n', '')
