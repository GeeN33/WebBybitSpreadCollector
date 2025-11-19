from time import sleep

from moex_grid.lib.bot import Bot


def startBot(name):
    bot = Bot(name)
    sleep(2)
    bot.setInfo()





