from datetime import datetime, timezone, timedelta
from time import sleep
from typing import List, Dict

import requests

import requests

from binans.models import InstrumentBinans, BarSpreadBinans


def getPrices()->List:

    API_URL = f"https://fapi.binance.com/fapi/v1/ticker/bookTicker"

    try:

        response = requests.get(API_URL)
        response.raise_for_status()
        response.json()

        # Получаем JSON-данные
        data = response.json()

        return data
    except Exception as e:
         print('Ошибка при загрузке страницы: ' + str(e))
         return []


def upDataBarSpread(instrument: InstrumentBinans, jsonPrices:List) -> bool:
    now = datetime.now(timezone.utc)
    # print(instrument.symbol1, instrument.symbol2)
    askPrice1 = 0
    bidPrice1 = 0
    askPrice2 = 0
    bidPrice2 = 0

    try:
        for price in jsonPrices:
            if price['symbol'] == instrument.symbol1:
                askPrice1 = float(price['askPrice'])
                bidPrice1 = float(price['bidPrice'])
            if price['symbol'] == instrument.symbol2:
                askPrice2 = float(price['askPrice'])
                bidPrice2 = float(price['bidPrice'])
    except Exception as e:
        return False

    # print(askPrice1, bidPrice1, askPrice2, bidPrice2)

    if  askPrice1 == 0 or bidPrice1 == 0 or askPrice2 == 0 or bidPrice2 == 0:
        return True

    bar = BarSpreadBinans.objects.filter(symbol_id=instrument.id).last()

    if bar:
        # print(now , bar.updated_at, timedelta(hours=1))
        if now - bar.created_at >= timedelta(hours=1):
            open = ((askPrice1 - bidPrice2) + (bidPrice1 - askPrice2)) / 2
            low = askPrice1 - bidPrice2
            high = bidPrice1 - askPrice2
            BarSpreadBinans.objects.create(symbol_id=instrument.id,
                                     per="1h",
                                     open=open,
                                     high=low,
                                     low=high,
                                     close=open)
        else:
            close = ((askPrice1 - bidPrice2) + (bidPrice1 - askPrice2)) / 2
            low = askPrice1 - bidPrice2
            high = bidPrice1 - askPrice2
            bar.close = close
            if bar.high < high:
                bar.high = high

            if bar.low > low:
                bar.low = low

            bar.save()

    else:
        open = ((askPrice1 - bidPrice2) + (bidPrice1 - askPrice2)) / 2
        low = askPrice1 - bidPrice2
        high = bidPrice1 - askPrice2
        BarSpreadBinans.objects.create(symbol_id=instrument.id,
                                 per="1h",
                                 open=open,
                                 high=low,
                                 low=high,
                                 close=open)

    instrument.is_updata = True
    instrument.save()
    return True


def upDataBarSpreadBinansStart():
    jsonPrices = getPrices()

    if len(jsonPrices) == 0: return 'Not data'

    instruments = InstrumentBinans.objects.filter(is_active=True)
    if instruments.filter(is_updata=False).exists():
        instruments = instruments.filter(is_updata=False)
    else:
        instruments.update(is_updata=False)

    for instrument in instruments:
        if upDataBarSpread(instrument, jsonPrices) == False:
            return 'Up data Break'

    return 'Up data Ok'