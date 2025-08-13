from datetime import datetime, timezone, timedelta
from time import sleep
from typing import Union,List, Dict
from django.db.models import QuerySet

import requests

from gateio.models import InstrumentGateio, PairGateio, BarSpreadGateio


def getInstrumentsGateio()-> List:
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/delivery/usdt/contracts'
    query_param = ''
    try:
        response = requests.request('GET', host + prefix + url, headers=headers)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print('Ошибка при загрузке страницы: ' + str(e))
        return []

def upDataInstrumentItem(base_symbol:str, instruments: Union[QuerySet, List[InstrumentGateio]]):
    # print('////////////////////////////////')
    PairGateio.objects.filter(base_symbol=base_symbol).update(is_active=False)
    instruments = instruments.filter(underlying=base_symbol).order_by('-expire_time')
    instrumentNames = []
    for instrument in instruments:
        defaultData={
            'base_symbol':base_symbol,
            'delivery1': True,
            'delivery2': False,
            'is_updata': True,
            'is_active': True,
        }
        PairGateio.objects.update_or_create(symbol1=instrument.name, symbol2=base_symbol, defaults=defaultData)
        instrumentNames.append(instrument.name)
        # print(instrument.name)

    for i in range(len(instrumentNames) - 1):
        for j in range(i + 1, len(instrumentNames)):
            # print(i, j)
            defaultData = {
                'base_symbol': base_symbol,
                'delivery1': True,
                'delivery2': True,
                'is_updata': True,
                'is_active': True,
            }
            PairGateio.objects.update_or_create(symbol1=instrumentNames[i], symbol2=instrumentNames[j], defaults=defaultData)

def upDataInstrumentGateio():
    InstrumentGateio.objects.all().update(is_active=False)
    instruments = getInstrumentsGateio()

    # print(len(instruments))

    for instrument in instruments:
        name = instrument.pop('name')
        instrument['is_active'] = True
        instrument['is_updata'] = True
        if name:
            InstrumentGateio.objects.update_or_create(name=name, defaults=instrument)

    instruments = InstrumentGateio.objects.filter(in_delisting=False, is_active=True)

    instrumentNameList = instruments.values_list('underlying', flat=True).distinct()

    for instrumentName in instrumentNameList:
        upDataInstrumentItem(instrumentName, instruments)

    return 'Up Instrument Gateio Ok'

def getPricesDelivery(contract)->dict:
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/delivery/usdt/order_book'
    query_param = f'contract={contract}&limit=1'
    try:
        data = {'symbol': contract, 'ask': 0, 'bid': 0 }
        response = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
        response.raise_for_status()
        res = response.json()
        if res.get('asks'):
            asks = res.get('asks')
            if len(asks) > 0:
               p = asks[0].get('p')
               data['ask'] = float(p)

        if res.get('bids'):
            bids = res.get('bids')
            if len(bids) > 0:
               p = bids[0].get('p')
               data['bid'] = float(p)

        return data

    except Exception as e:
        return {}
def getPricesFutures(contract)->dict:
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/futures/usdt/order_book'
    query_param = f'contract={contract}&limit=1'
    try:
        data = {'symbol': contract, 'ask': 0, 'bid': 0}
        response = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
        response.raise_for_status()
        res = response.json()
        if res.get('asks'):
            asks = res.get('asks')
            if len(asks) > 0:
                p = asks[0].get('p')
                data['ask'] = float(p)

        if res.get('bids'):
            bids = res.get('bids')
            if len(bids) > 0:
                p = bids[0].get('p')
                data['bid'] = float(p)

        return data

    except Exception as e:
        return {}

def upDataBarSpreadGateioItem(base_symbol:str):
    # print(base_symbol)
    pricesGateio = {}
    p = getPricesFutures(base_symbol)
    if p.get('symbol') and p.get('ask', 0) != 0 and p.get('bid', 0) != 0:
        pricesGateio[p['symbol']] = p

    pairs = PairGateio.objects.filter(is_updata=True, is_active=True, base_symbol=base_symbol)
    pairsNameList = set()
    for pair in pairs:
        if pair.delivery1:
            pairsNameList.add(pair.symbol1)
        if pair.delivery2:
            pairsNameList.add(pair.symbol2)
    for pairName in pairsNameList:
        sleep(1)
        p = getPricesDelivery(pairName)
        if p.get('symbol') and p.get('ask', 0) != 0 and p.get('bid', 0) != 0:
            pricesGateio[p['symbol']] = p

    now = datetime.now(timezone.utc)
    for pair in pairs:
        if pricesGateio.get(pair.symbol1) and pricesGateio.get(pair.symbol2):
            ask1 = pricesGateio.get(pair.symbol1, {}).get('ask')
            bid1 = pricesGateio.get(pair.symbol1, {}).get('bid')
            ask2 = pricesGateio.get(pair.symbol2, {}).get('ask')
            bid2 = pricesGateio.get(pair.symbol2, {}).get('bid')

            ask = ask1 - bid2
            bid = bid1 - ask2

            last1 = (ask1 + bid1) / 2
            last2 = (ask2 + bid2) / 2

            bar = BarSpreadGateio.objects.filter(symbol_id=pair.id).last()
            if bar:
                if now - bar.created_at >= timedelta(hours=1):
                    open = (ask + bid) / 2
                    BarSpreadGateio.objects.create(symbol_id=pair.id,
                                             per="1h",
                                             open=open,
                                             high=bid,
                                             low=ask,
                                             close=open,
                                             last1=last1,
                                            last2=last2)
                else:
                    bar.close = (ask + bid) / 2
                    if bar.high < bid:
                        bar.high = bid

                    if bar.low > ask:
                        bar.low = ask

                    bar.last1 = last1
                    bar.last2 = last2

                    bar.save()
            else:
                open = (ask + bid) / 2
                BarSpreadGateio.objects.create(symbol_id=pair.id,
                                         per="1h",
                                         open=open,
                                         high=ask,
                                         low=bid,
                                         close=open)

    # print(pricesGateio)
def upDataBarSpreadGateioStart():
    instruments = InstrumentGateio.objects.filter(in_delisting=False, is_active=True)

    instrumentNameList = instruments.values_list('underlying', flat=True).distinct()

    for instrumentName in instrumentNameList:
        upDataBarSpreadGateioItem(instrumentName)

    return 'Up BarSpreadGateio Ok'