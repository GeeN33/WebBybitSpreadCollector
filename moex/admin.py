from django.contrib import admin

from moex.models import BotSpreadBollinger, BollingerLevel

admin.site.register(BotSpreadBollinger)

admin.site.register(BollingerLevel)