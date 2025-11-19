from typing import List, Optional

import requests

from moex.lib.authentication import Auth
from moex.lib.modelsPy import Order
from moex.models import BotSpreadBollinger, BollingerLevel


class Bot(Auth):
    def __init__(self, name):
        super().__init__(name)

    def get_account_info(self, account_id) -> dict:
        url = f"https://api.finam.ru/v1/accounts/{account_id}"

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

    def get_last_quote(self, symbol) -> dict:

        url = f"https://api.finam.ru/v1/instruments/{symbol}/quotes/latest"

        headers = {
            "Authorization": self.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            quote = response.json()  # Получаем JSON-ответ
            return quote
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return {}

    def setInfo(self):

        info = self.get_account_info(self.bollinger.account_id)

        side = 'n'
        value = 0
        positions = info.get('positions', [])
        symbol1 = 0
        symbol2 = 0
        values = []
        for position in positions:
            if self.bollinger.symbol1 == position.get('symbol', ''):
                symbol1 = position.get('quantity', {}).get('value', 0)
                symbol1 = float(symbol1)
                values.append(abs(symbol1))
            if self.bollinger.symbol2 == position.get('symbol', ''):
                symbol2 = position.get('quantity', {}).get('value', 0)
                symbol2 = float(symbol2)
                values.append(abs(symbol2))

        if symbol1 > 0 and symbol2 < 0:
            side = 'b'
        if symbol1 < 0 and symbol2 > 0:
            side = 's'

        if values:
            value = min(values)

        BotSpreadBollinger.objects.filter(id=self.bollinger.id).update(side=side, value=value)

        base_symbol = self.get_last_quote(self.bollinger.base_symbol)
        if base_symbol and 'symbol' in base_symbol and base_symbol.get('symbol') == self.bollinger.base_symbol:
            ask = base_symbol.get('quote', {}).get('ask', {}).get('value', 0)
            last = base_symbol.get('quote', {}).get('last', {}).get('value', 0)
            bid = base_symbol.get('quote', {}).get('bid', {}).get('value', 0)

            BotSpreadBollinger.objects.filter(id=self.bollinger.id).update(ask=ask, last=last, bid=bid)

    def levelWork(self):

        try:
            self.bollinger = BotSpreadBollinger.objects.get(id=self.bollinger.id)
        except BotSpreadBollinger.DoesNotExist:
            return

        levels = BollingerLevel.objects.filter(bot=self.bollinger)

        level_sort = []

        for level in levels:
            if level.normal_price - self.bollinger.ask > 0:
                level_sort.append({
                    'level_id': level.level_id,
                    'price': level.normal_price - self.bollinger.ask
                })

        min_level = min(level_sort, key=lambda x: x['price'])
        BollingerLevel.objects.filter(bot=self.bollinger).exclude(level_id=min_level.get('level_id', 0)).update(
            level_stop_high=False)
        BollingerLevel.objects.filter(bot=self.bollinger, level_id=min_level.get('level_id', 0)).update(level_stop_high=True)

        level_sort = []

        for level in levels:
            if self.bollinger.bid - level.normal_price > 0:
                level_sort.append({
                    'level_id': level.level_id,
                    'price': self.bollinger.bid - level.normal_price
                })

        min_level = min(level_sort, key=lambda x: x['price'])

        BollingerLevel.objects.filter(bot=self.bollinger).exclude(level_id=min_level.get('level_id', 0)).update(
            level_stop_low=False)
        BollingerLevel.objects.filter(bot=self.bollinger, level_id=min_level.get('level_id', 0)).update(level_stop_low=True)

    def levelLimitUp(self):
        try:
            self.bollinger = BotSpreadBollinger.objects.get(id=self.bollinger.id)
        except BotSpreadBollinger.DoesNotExist:
            return

        lot_max = self.bollinger.lot_max
        lot_work = self.bollinger.lot_work
        side = self.bollinger.side
        value = self.bollinger.value

        levels = BollingerLevel.objects.filter(bot=self.bollinger)
        BollingerLevel.objects.filter(bot=self.bollinger).update(quantity=0, level_side='n')

        # //////////

        levels_high = levels.order_by('level_high')

        if side == 'b':
            valueAll_high = lot_max + value
        else:
            valueAll_high = lot_max - value

        for level in levels_high:
            if valueAll_high > 0:
                if level.level_stop_high:
                    BollingerLevel.objects.filter(id=level.id).update(limit_price=level.normal_price,
                                                                      quantity=valueAll_high, level_side='s')
                    break
                else:
                    valueAll_high -= lot_work
                    BollingerLevel.objects.filter(id=level.id).update(limit_price=level.normal_price, quantity=lot_work,
                                                                      level_side='s')

        # //////

        levels_low = levels.order_by('level_low')

        if side == 's':
            valueAll_low = lot_max + value
        else:
            valueAll_low = lot_max - value

        for level in levels_low:
            if valueAll_low > 0:
                if level.level_stop_high:
                    BollingerLevel.objects.filter(id=level.id).update(limit_price=level.normal_price,
                                                                      quantity=valueAll_low, level_side='b')
                    break
                else:
                    valueAll_low -= lot_work
                    BollingerLevel.objects.filter(id=level.id).update(limit_price=level.normal_price, quantity=lot_work,
                                                                      level_side='b')

    def get_orders(self) -> List[Order]:

        account_id = self.bollinger.account_id

        url = f"https://api.finam.ru/v1/accounts/{account_id}/orders"

        headers = {
            "Authorization": self.jwt_token
        }

        orders_list: List[Order] = []
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            account_info = response.json()  # Получаем JSON-ответ
            orders = account_info.get('orders', [])
            # print(orders)
            for ord in orders:
                order_id = ord.get('order_id', '')
                status = ord.get('status', '')
                order = ord.get('order', {})
                if self.bollinger.account_id == order.get('account_id', '') and self.bollinger.base_symbol == order.get('symbol', ''):
                    account_id = order.get('account_id', '')
                    symbol = order.get('symbol', '')
                    side = order.get('side', '')
                    order_type = order.get('type', '')
                    limit_price = float(order.get('limit_price', {}).get('value', 0))
                    quantity = float(order.get('quantity', {}).get('value', 0))
                    orders_list.append(
                        Order(
                        order_id=order_id,
                        account_id=account_id,
                        symbol=symbol,
                        side=side,
                        status=status,
                        order_type=order_type,
                        limit_price=limit_price,
                        quantity=quantity
                    ))

            return orders_list

        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return []

    def place_order(self, side, limit_price, quantity)-> Optional[Order]:

        symbol = self.bollinger.base_symbol

        account_id = self.bollinger.account_id

        url = f"https://api.finam.ru/v1/accounts/{account_id}/orders"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.jwt_token
        }
        data = {

            "symbol": symbol,
            "quantity": {
                "value": str(quantity)
            },
            "side": side,
            "type": "ORDER_TYPE_LIMIT",
            "timeInForce": "TIME_IN_FORCE_DAY",
            "limitPrice": {
                "value": str(limit_price)
            },
            "stopCondition": "STOP_CONDITION_UNSPECIFIED",
            "legs": []
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            ord = response.json()
            order_id = ord.get('order_id', '')
            status = ord.get('status', '')
            order = ord.get('order', {})
            account_id = order.get('account_id', '')
            symbol = order.get('symbol', '')
            side = order.get('side', '')
            order_type = order.get('type', '')
            limit_price = float(order.get('limit_price', {}).get('value', 0))
            quantity = float(order.get('quantity', {}).get('value', 0))

            return Order(
                        order_id=order_id,
                        account_id=account_id,
                        symbol=symbol,
                        side=side,
                        status=status,
                        order_type=order_type,
                        limit_price=limit_price,
                        quantity=quantity
                    )
        else:
            # Обработка ошибок
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None

    def cancel_order(self, order_id):

        account_id = self.bollinger.account_id

        url = f"https://api.finam.ru/v1/accounts/{account_id}/orders/{order_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.jwt_token
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:

            return response.json()

        else:
            # Обработка ошибок
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None

