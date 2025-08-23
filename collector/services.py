from datetime import datetime, timezone, timedelta
from time import sleep
from typing import List, Dict, Union

import requests
from django.db.models import QuerySet

from collector.models import Instrument, BarSpread
from collector.utils import timestampToDate


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
        # print(data)
        # Извлекаем необходимые значения
        # Извлекаем необходимые значения
        if data['retCode'] == 0 and 'list' in data['result'] and 'time' in data:
            # Предполагаем, что интересующая нас информация в первом элементе списка
            bidPrice = None
            askPrice = None
            lastPrice = None

            ticker_info = data['result']['list'][0]
            if ticker_info.get('bidPrice'):
                bidPrice = float(ticker_info.get('bidPrice', 0))
            if ticker_info.get('askPrice'):
              askPrice = float(ticker_info.get('askPrice', 0))

            if ticker_info.get('lastPrice'):
               lastPrice = float(ticker_info.get('lastPrice', 0))

            if bidPrice == None:
                if lastPrice:
                    bidPrice = lastPrice

            if askPrice == None:
                if lastPrice:
                    askPrice = lastPrice

            if bidPrice and askPrice:
                return {
                    'bidPrice': bidPrice,
                    'askPrice': askPrice,
                }
            else:
                return {}
        else:
            return {}
    except Exception as e:
         print('Ошибка при загрузке страницы: ' + str(e))
         return {}

def upDataBarSpread(instrument:Instrument)->bool:
    now = datetime.now(timezone.utc)
    # print(instrument.symbol)
    jsonPrices = getPrice(instrument.symbol)
    # print(jsonPrices)

    if jsonPrices and 'askPrice' in  jsonPrices and 'bidPrice' in  jsonPrices:
        sleep(1)
    else:
        instrument.is_updata = True
        instrument.save()
        sleep(10)


    bar = BarSpread.objects.filter(symbol_id=instrument.id).order_by('updated_at').last()

    if bar:
        # print(now , bar.updated_at, timedelta(hours=1))
        if now - bar.created_at >= timedelta(hours=1):
            open = (jsonPrices['askPrice'] + jsonPrices['bidPrice']) / 2
            BarSpread.objects.create(symbol_id=instrument.id,
                                        per="1h",
                                        open = open,
                                        high = jsonPrices['bidPrice'],
                                        low = jsonPrices['askPrice'],
                                        funding = bar.funding,
                                        fair1 = bar.fair1,
                                        fair2 = bar.fair2,
                                        close =open)
        else:
          bar.close = (jsonPrices['askPrice'] + jsonPrices['bidPrice']) / 2
          if bar.high < jsonPrices['bidPrice']:
              bar.high = jsonPrices['bidPrice']

          if bar.low > jsonPrices['askPrice']:
              bar.low = jsonPrices['askPrice']

          bar.save()

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

def getPricePERP(symbol)->float:

    API_URL = f"https://api.bybit.com/v5/market/tickers?category=inverse&symbol={symbol}"

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
            lastPrice = float(ticker_info.get('lastPrice', 0))

            return lastPrice
        else:
            return 0
    except Exception as e:
         print('Ошибка при загрузке страницы: ' + str(e))
         return 0

def getFunding(symbol)-> float:

    API_URL = f"https://api.bybit.com/v5/market/funding/history?category=linear&symbol={symbol}PERP&limit=3"
    try:

        response = requests.get(API_URL)
        response.raise_for_status()
        response.json()

        fundings = response.json().get('result', {}).get('list', [])
        sam = 0

        for funding in fundings:
            sam += float(funding.get('fundingRate', 0))

        return sam

    except Exception as e:
        print('Ошибка при загрузке страницы: ' + str(e))
        return 0

def upDataFundingItem(base_symbol:str, instruments: Union[QuerySet, List[Instrument]]):

    dateNew = datetime.utcnow()

    funding = getFunding(base_symbol)
    sleep(1)
    price = getPricePERP(base_symbol + 'USDT')

    instruments = instruments.filter(contract_type='PerpBasis', base_coin=base_symbol)
    for instrument in instruments:
        difference = timestampToDate(instrument.delivery_time) - dateNew
        days_between = difference.days
        priceAll = price * funding * days_between
        sleep(0.1)
        bar = BarSpread.objects.filter(symbol_id=instrument.id).order_by('updated_at').last()
        if bar:
            bar.funding = priceAll
            bar.save()
            # print(instrument.symbol, difference, priceAll)

def upDataFundingStart():
    instruments = Instrument.objects.filter(is_active=True)
    instrumentNameList = instruments.values_list('base_coin', flat=True).distinct()

    for instrumentName in instrumentNameList:
        sleep(1)
        upDataFundingItem(instrumentName, instruments)

    return 'Up Data Funding Ok'

    # # Ваша метка времени в миллисекундах
    # timestamp_ms = 1782457200000
    #
    # date_time = timestampToDate(timestamp_ms)
    #
    # print(date_time.strftime('%Y-%m-%d %H:%M:%S'))


