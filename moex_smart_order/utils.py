from datetime import datetime, time, timedelta
import pytz

def round_price(price, step):

    remainder = int(price / step)

    rounded_price = remainder * step

    size = len(str(step).split('.')[-1])

    return round(rounded_price, size)

def is_within_schedule():
    # Устанавливаем часовой пояс для Москвы
    moscow_tz = pytz.timezone('Europe/Moscow')

    # Получаем текущее время в московском часовом поясе
    now = datetime.now(moscow_tz)

    # Дни недели: 0 - понедельник, 1 - вторник, ..., 5 - суббота, 6 - воскресенье
    weekday = now.weekday()

    # Устанавливаем временные рамки для будних дней и выходных
    if weekday < 5:  # Если это будний день
        start_time = time(9, 1)  # 9:00 утра
        end_time = time(20, 59)  # 8:59 ночи (практически 9:00)
    else:  # Если это выходной (суббота или воскресенье)
        start_time = time(10, 1)  # 10:00 утра
        end_time = time(19, 0)  # 7:00 вечера

    # Проверяем, находится ли текущее время в указанных пределах
    return start_time <= now.time() <= end_time