from time import sleep

from moex.lib.bollinger import Bollinger
from moex.lib.bot import Bot
from moex.models import BotSpreadBollinger, BollingerLevel
from moex.utils import filter_order


def startBot(name):
    bot = Bot(name)
    sleep(2)
    bot.setInfo()

    jwt_token = bot.jwt_token
    bollinger = bot.bollinger
    bot.levelWork()
    bot.levelLimitUp()

    orders = bot.get_orders()
    for order in orders:
       print(order)

    levels = BollingerLevel.objects.filter(bot=bollinger)
    for level in levels:
        orders, order = filter_order(orders,
                                     level.order_id,
                                     level.side,
                                     level.limit_price,
                                     level.quantity)
        if order:
            print('OLD', order)
            BollingerLevel.objects.filter(order_id=order.order_id).update(status=order.status, quantity=order.quantity)
        else:
            side = None
            if level.level_side == 'b':
                side = 'SIDE_BUY'
            if level.level_side == 's':
                side = 'SIDE_SELL'
            if side and level.normal_price and level.quantity:
                sleep(2)
                order = bot.place_order(side, level.normal_price, level.quantity)
                if order:
                    print('NEW', order)
                    BollingerLevel.objects.filter(id=level.id).update(
                                                                order_id=order.order_id,
                                                                status = order.status,
                                                                order_type = order.order_type,
                                                                side = order.side,
                                                                limit_price = order.limit_price,
                                                                quantity = order.quantity)

    for order in orders:
        if order.status == 'ORDER_STATUS_NEW' or order.status == 'ORDER_STATUS_PARTIALLY_FILLED':
            print('cancel_order', order)
            bot.cancel_order(order.order_id)


def startBollinger(name):

    Bollinger(name).setBollinger()

    sleep(2)

    startBot(name)











