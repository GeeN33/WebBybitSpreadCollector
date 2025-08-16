from datetime import datetime


def timestampToDate(timestamp_ms) -> datetime:
    # Преобразуем миллисекунды в секунды
    timestamp_s = timestamp_ms / 1000.0

    # Создаем объект datetime из метки времени
    return datetime.fromtimestamp(timestamp_s)


