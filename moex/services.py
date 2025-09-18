from time import sleep

from moex.lib.bollinger import Bollinger
from moex.lib.bot import Bot
from moex.models import BotSpreadBollinger, BollingerLevel


def startBot(name):
    bot = Bot(name)
    sleep(2)
    bot.setInfo()

    jwt_token = bot.jwt_token
    bollinger = bot.bollinger
    bot.levelWork()
    bot.levelLimitUp()


    levels = BollingerLevel.objects.filter(bot=bollinger)
    for level in levels:
        print(level)

def startBollinger(name):

    Bollinger(name).setBollinger()

    sleep(2)

    startBot(name)









