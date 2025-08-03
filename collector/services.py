from datetime import datetime, timezone, timedelta
from time import sleep
from typing import List, Dict

import requests
from collector.models import Instrument, BarSpread


def getInstruments()-> List:
    API_URL = f"https://api.bybit.com/v5/spread/instrument"
    try:

        response = requests.get(API_URL)
        response.raise_for_status()
        response.json()

        instruments = response.json().get('result', {}).get('list', [])

        return instruments

    except Exception as e:
        print('Ошибка при загрузке страницы: ' + str(e))
        return []

def upDataInstrument():
    Instrument.objects.all().update(is_active=False)

    instruments = getInstruments()

    for instrument in instruments:
        data = instrument

        instr, create = Instrument.objects.update_or_create(
            symbol=data.get('symbol', ''),
            defaults={
                'contract_type': data.get('contractType', ''),
                'status': data.get('status', ''),
                'base_coin': data.get('baseCoin', ''),
                'quote_coin': data.get('quoteCoin', ''),
                'settle_coin': data.get('settleCoin', ''),
                'tick_size': float(data.get('tickSize', 0)),
                'min_price': float(data.get('minPrice', 0)),
                'max_price': float(data.get('maxPrice', 0)),
                'lot_size': float(data.get('lotSize', 0)),
                'min_size': float(data.get('minSize', 0)),
                'max_size': float(data.get('maxSize', 0)),
                'launch_time': int(data.get('launchTime', 0)),
                'delivery_time': int(data.get('deliveryTime', 0)),
                'legs': data.get('legs', []),
                'is_active': True
            }
        )

        # if create:
        #     print(instr.symbol)


def getPrice(symbol)->Dict:

    API_URL = f"https://api.bybit.com/v5/spread/tickers?symbol={symbol}"

    try:

        response = requests.get(API_URL)
        response.raise_for_status()
        response.json()

        # Получаем JSON-данные
        data = response.json()

        # Извлекаем необходимые значения
        # Извлекаем необходимые значения
        if data['retCode'] == 0 and 'list' in data['result'] and 'time' in data:
            # Предполагаем, что интересующая нас информация в первом элементе списка
            ticker_info = data['result']['list'][0]
            bidPrice = float(ticker_info.get('bidPrice', 0))
            bidSize = float(ticker_info.get('bidSize', 0))
            askPrice = float(ticker_info.get('askPrice', 0))
            askSize = float(ticker_info.get('askSize', 0))
            # lastPrice = float(ticker_info.get('lastPrice', 0))

            return {
                'bidPrice': bidPrice,
                'bidSize': bidSize,
                'askPrice': askPrice,
                'askSize': askSize,
                 # 'lastPrice': lastPrice,
            }
        else:
            return {}
    except Exception as e:
         print('Ошибка при загрузке страницы: ' + str(e))
         return {}

def upDataBarSpread(instrument:Instrument)->bool:
    now = datetime.now(timezone.utc)
    # print(instrument.symbol)
    jsonPrices = getPrice(instrument.symbol)
    if jsonPrices:
        sleep(1)
    else:
        instrument.is_updata = True
        instrument.save()
        return False

    bar = BarSpread.objects.filter(symbol_id=instrument.id).last()

    if bar:
        # print(now , bar.updated_at, timedelta(hours=1))
        if now - bar.updated_at >= timedelta(hours=1):
            open = (jsonPrices['askPrice'] + jsonPrices['bidPrice']) / 2
            BarSpread.objects.create(symbol_id=instrument.id,
                                        per="1h",
                                        open = open,
                                        high = jsonPrices['bidPrice'],
                                        low = jsonPrices['askPrice'],
                                        close =open)
        else:
          bar.close = (jsonPrices['askPrice'] + jsonPrices['bidPrice']) / 2
          if bar.high < jsonPrices['bidPrice']:
              bar.high = jsonPrices['bidPrice']

          if bar.low > jsonPrices['askPrice']:
              bar.low = jsonPrices['askPrice']

    else:
        open = (jsonPrices['askPrice'] + jsonPrices['bidPrice']) / 2
        BarSpread.objects.create(symbol_id=instrument.id,
                                 per="1h",
                                 open=open,
                                 high=jsonPrices['bidPrice'],
                                 low=jsonPrices['askPrice'],
                                 close=open)

    instrument.is_updata = True
    instrument.save()
    return True
        

def upDataBarSpreadStart():
    instruments = Instrument.objects.filter(is_active=True)
    if instruments.filter(is_updata=False).exists():
        instruments = instruments.filter(is_updata=False)
    else:
        instruments.update(is_updata=False)


    for instrument in instruments:
         if upDataBarSpread(instrument) == False:
             return 'Up data Break'


    return 'Up data Ok'