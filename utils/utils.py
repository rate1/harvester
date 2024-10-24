def split_text(text: str, max_len: int) -> list[str]:
    """
    Разбивает текст на части, чтобы каждая часть не превышала max_len символов.
    Args:
        text (str): Исходный текст.
        max_len (int): Максимальная длина одной части.
    Returns:
        list[str]: Список частей текста.
    """
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]
