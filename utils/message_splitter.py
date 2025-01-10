def split_text(text: str, max_length: int = 4096) -> list[str]:
    """Разделяет сообщение на части, сохраняя правильную разметку HTML."""
    parts = []
    start = 0
    while start < len(text):
        end = start + max_length
        if end > len(text):
            end = len(text)
        else:
            # Найти ближайший пробел или символ новой строки перед end
            while end > start and text[end] not in (' ', '\n'):
                end -= 1
            if end == start:
                end = start + max_length  # Если нет пробелов, разбиваем по max_length
        parts.append(text[start:end])
        start = end
    return parts
