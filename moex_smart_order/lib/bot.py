from typing import List, Optional

import requests

from moex_smart_order.lib.authentication import Auth
from moex_smart_order.lib.modelsPy import Order
from moex_smart_order.models import BotSmart


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

    def get_assets(self, account_id, symbol):

        url = f"https://api.finam.ru/v1/assets/{symbol}/params?account_id={account_id}"

        headers = {
            "Authorization": self.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            info = response.json()  # Получаем JSON-ответ
            return info
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return None

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

        assets = self.get_assets(self.auth_bot.account_id, self.bot.base_symbol)
        # print(assets)
        if assets and 'tradeable' in assets:

            self.is_assets = assets.get('tradeable', False)

        if self.is_assets == False: return None

        info = self.get_account_info(self.auth_bot.account_id)

        side = 'n'
        value = 0
        positions = info.get('positions', [])
        symbol1 = 0
        symbol2 = 0
        values = []
        for position in positions:
            if self.bot.symbol1 == position.get('symbol', ''):
                symbol1 = position.get('quantity', {}).get('value', 0)
                symbol1 = float(symbol1)
                values.append(abs(symbol1))
            if self.bot.symbol2 == position.get('symbol', ''):
                symbol2 = position.get('quantity', {}).get('value', 0)
                symbol2 = float(symbol2)
                values.append(abs(symbol2))

        if symbol1 > 0 and symbol2 < 0:
            side = 'b'
        if symbol1 < 0 and symbol2 > 0:
            side = 's'

        if values:
            value = min(values)

        BotSmart.objects.filter(id=self.bot.id).update(side=side, value=value)

    def setQuote(self):

        base_symbol = self.get_last_quote(self.bot.base_symbol)
        if base_symbol and 'symbol' in base_symbol and base_symbol.get('symbol') == self.bot.base_symbol:
            ask = base_symbol.get('quote', {}).get('ask', {}).get('value', 0)
            last = base_symbol.get('quote', {}).get('last', {}).get('value', 0)
            bid = base_symbol.get('quote', {}).get('bid', {}).get('value', 0)

            BotSmart.objects.filter(id=self.bot.id).update(ask=ask, last=last, bid=bid)

        try:
            self.bot = BotSmart.objects.get(id=self.bot.id)
        except BotSmart.DoesNotExist:
            pass

    def get_orders(self) -> List[Order]:

        account_id = self.auth_bot.account_id

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
                if self.auth_bot.account_id == order.get('account_id', '') and self.bot.base_symbol == order.get('symbol', ''):
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

        symbol = self.bot.base_symbol

        account_id = self.auth_bot.account_id

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

        account_id = self.auth_bot.account_id

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
