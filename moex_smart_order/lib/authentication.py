from datetime import datetime, timedelta

import requests

from moex.models import BotAuth
from moex_smart_order.models import BotSmart


class Auth:
    def __init__(self, name):

        self.jwt_token = None
        self.is_active = False
        self.is_assets = False
        self.bot: BotSmart
        self.auth_bot: BotAuth

        try:
            self.bot = BotSmart.objects.get(name=name)
            self.is_active = self.bot.is_active
        except BotSmart.DoesNotExist:
            self.is_active = False

        if self.is_active:
            try:
                self.auth_bot = BotAuth.objects.get(id=self.bot.auth_bot.id)
            except BotAuth.DoesNotExist:
                self.is_active = False

            token_details = self.get_token_details(self.auth_bot.jwt_token)

            if token_details and token_details.get('expires_at') and self.is_token_valid(token_details):
                self.jwt_token = self.auth_bot.jwt_token
            else:
                self.jwt_token = self.get_jwt_token(self.auth_bot.secret_key)
                if self.jwt_token:
                    BotAuth.objects.filter(id=self.auth_bot.id).update(jwt_token=self.jwt_token)
                else:
                    self.is_active = False

    def get_jwt_token(self, secret_key) -> str | None:
        url = "https://api.finam.ru/v1/sessions"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "secret": secret_key
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            # Извлечение JWT токена из ответа
            if response_json and "token" in  response_json:
                 token = response_json.get("token")
                 return token
            else:
                return None
        else:
            # Обработка ошибок
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None
    def is_token_valid(self, token_info) -> bool:
        # Преобразуем время из строки в объект datetime
        expires_at = datetime.strptime(token_info['expires_at'], '%Y-%m-%dT%H:%M:%SZ')

        # Получаем текущее время в UTC
        current_time = datetime.utcnow()

        # print(expires_at - current_time)

        five_minutes = timedelta(minutes=5)
        # Сравниваем текущее время с временем истечения
        return current_time < (expires_at - five_minutes)
    def get_token_details(self, jwt_token) -> dict:
        url = "https://api.finam.ru/v1/sessions/details"

        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "token": jwt_token
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            token = response.json()
            return token
        else:
            return {}