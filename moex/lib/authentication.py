from datetime import datetime, timedelta

import requests

from moex.models import BotSpreadBollinger


class Auth:
    def __init__(self, name):

        self.jwt_token = None

        self.bollinger: BotSpreadBollinger

        try:
            self.bollinger = BotSpreadBollinger.objects.get(name=name)
        except BotSpreadBollinger.DoesNotExist:
            self.jwt_token = None

        if  self.bollinger:
            token_details = self.get_token_details(self.bollinger.jwt_token)

            if token_details and token_details.get('expires_at') and self.is_token_valid(token_details):
                self.jwt_token = self.bollinger.jwt_token
            else:
                self.jwt_token = self.get_jwt_token(self.bollinger.secret_key)
                BotSpreadBollinger.objects.filter(id=self.bollinger.id).update(jwt_token=self.jwt_token)

    def get_jwt_token(self, secret_key) -> str:
        url = "https://api.finam.ru/v1/sessions"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "secret": secret_key
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Извлечение JWT токена из ответа
            token = response.json().get("token")
            return token
        else:
            # Обработка ошибок
            print(f"Ошибка: {response.status_code}, {response.text}")
            return ''
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