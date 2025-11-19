from datetime import datetime, timedelta

import requests

from moex.lib.authentication import Auth
from moex.models import BollingerLevel
from moex.utils import round_price
import statistics


class Bollinger(Auth):
    def __init__(self, name):
        super().__init__(name)

    def get_bars(self, symbol, start_time, end_time, timeframe) -> dict:

        url = f"https://api.finam.ru/v1/instruments/{symbol}/bars?interval.start_time={start_time}&interval.end_time={end_time}&timeframe={timeframe}"

        headers = {
            "Authorization": self.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            account_info = response.json()  # Получаем JSON-ответ
            return account_info
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return {}

    def calculate_bollinger_bands(self, bars, period=20, deviation=2.0) -> list:
        closes = [float(bar['close']['value']) for bar in bars]

        if len(closes) < period:
            raise ValueError("Not enough data to calculate Bollinger Bands")

        bollinger_bands = []
        for i in range(period - 1, len(closes)):
            window_closes = closes[i - period + 1:i + 1]
            sma = sum(window_closes) / period
            std_dev = statistics.stdev(window_closes)
            upper_band = sma + (std_dev * deviation)
            lower_band = sma - (std_dev * deviation)
            bollinger_bands.append({
                'sma': sma,
                'upper_band': upper_band,
                'lower_band': lower_band
            })

        return bollinger_bands

    def setBollinger(self):

        now = datetime.utcnow()
        #
        # # Начальное время: текущее время минус 7 дней
        start_time = now - timedelta(days=15)
        # Конечное время: текущая дата и время
        end_time = now + timedelta(days=1)
        #
        # # Форматирование времени в строку с форматом ISO 8601
        start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time= end_time.strftime('%Y-%m-%dT%H:%M:%SZ')


        timeframe = 'TIME_FRAME_H1'

        bars = self.get_bars(self.bollinger.base_symbol, start_time, end_time, timeframe)
        bars = bars.get('bars', [])
        # print(bars)
        levels = BollingerLevel.objects.filter(bot=self.bollinger)

        for level in levels:
            bollinger_bands = self.calculate_bollinger_bands(bars, level.period, level.deviation)
            if len(bollinger_bands) > 0 and  level.level_type == "sma":
                level.level_price = bollinger_bands[len(bollinger_bands)-1].get('sma', 0)
                level.normal_price = round_price(level.level_price, self.bollinger.step_price)

            if len(bollinger_bands) > 0 and level.level_type == "high":
                level.level_price = bollinger_bands[len(bollinger_bands) - 1].get('upper_band', 0)
                level.normal_price = round_price(level.level_price, self.bollinger.step_price)

            if len(bollinger_bands) > 0 and level.level_type == "low":
                level.level_price = bollinger_bands[len(bollinger_bands) - 1].get('lower_band', 0)
                level.normal_price = round_price(level.level_price, self.bollinger.step_price)

            level.save()
