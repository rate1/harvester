import os

from openai import OpenAI


def gpt_rewrite(text):

    print(os.environ.get("OPENAI_API_KEY"))

    client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
    )
    # Вызов GPT для рерайта текста
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Или другой доступный движок GPT
        messages=[
            {
                "role": "system",
                "content": ("Ты David Ogilvy,занимаешься качественным "
                            "копирайтом текста. Профессионал своего дела.")
             },
             {
                 "role": "user",
                 "content": f"Переформулируй указанный после двоеточия текст и адаптируй его так, чтобы он идеально подходил для публикации в виде статьи на Яндекс.Дзен. Очеловечь этот текст и убери из него предложения лишенные смысла, оживи и создай сенсацию, чтобы текст вызывал желание дочитать статью до самого конца:\n\n{text}"
             }
        ],
        max_tokens=1000,
        temperature=0.7
    )

    return response.choices[0].message
