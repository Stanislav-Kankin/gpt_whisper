def split_text(text: str, max_length: int = 4096) -> list[str]:
    """
    Разбивает текст на части, не превышающие max_length символов.
    Если текст не содержит переносов строк, разбивает его на равные части.
    """
    parts = []
    while len(text) > max_length:
        # Ищем последний перенос строки в пределах max_length
        part = text[:max_length]
        last_newline = part.rfind("\n")
        last_space = part.rfind(" ")

        # Если есть перенос строки, разбиваем по нему
        if last_newline != -1:
            split_index = last_newline
        # Если есть пробел, разбиваем по нему
        elif last_space != -1:
            split_index = last_space
        # Если нет ни переноса строки, ни пробела, разбиваем по max_length
        else:
            split_index = max_length

        # Добавляем часть текста
        parts.append(text[:split_index].strip())
        text = text[split_index:].strip()

    # Добавляем оставшийся текст
    if text:
        parts.append(text)
    return parts
