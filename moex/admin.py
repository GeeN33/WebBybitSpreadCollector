from django.contrib import admin

from moex.models import BotAuth, BotSpreadBollinger, BollingerLevel

admin.site.register(BotAuth)

admin.site.register(BotSpreadBollinger)

admin.site.register(BollingerLevel)