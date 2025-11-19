from time import sleep

from moex.utils import filter_order, round_price
from moex_smart_order.lib.bot import Bot
from moex_smart_order.models import OrderSmart
from moex_smart_order.utils import is_within_schedule


# python manage.py start_bot_smart_test
def startSmartBot(name):
    if not is_within_schedule(): return
    bot = Bot(name)
    if not bot.is_active: return
    sleep(2)
    bot.setInfo()
    if not bot.is_assets: return
    sleep(2)
    orders = bot.get_orders()
    sleep(2)
    bot.setQuote()

    # for order in orders:
    #    print(order)

    step_price = bot.bot.step_price
    range_price = bot.bot.range_price
    side = bot.bot.side
    value = bot.bot.value
    ask = bot.bot.ask
    last = bot.bot.last
    bid = bot.bot.bid

    s_levels = OrderSmart.objects.filter(bot_id=bot.bot.id, level_side='s').order_by('level_queue')
    b_levels = OrderSmart.objects.filter(bot_id=bot.bot.id, level_side='b').order_by('level_queue')

    if len(s_levels) > 0:
        s_level = s_levels.first()
        if s_level.level_price > bid + range_price or s_level.level_price == 0:
            range_price_tem = bid
            for level in s_levels:
                range_price_tem = range_price_tem + range_price
                range_price_tem = round_price(range_price_tem, step_price)
                OrderSmart.objects.filter(id=level.id).update(level_price = range_price_tem)

    if len(b_levels) > 0:
        b_level = b_levels.first()
        if b_level.level_price < ask - range_price or b_level.level_price == 0:
            range_price_tem = ask
            for level in b_levels:
                range_price_tem = range_price_tem - range_price
                range_price_tem = round_price(range_price_tem, step_price)
                OrderSmart.objects.filter(id=level.id).update(level_price=range_price_tem)

    s_levels = OrderSmart.objects.filter(bot_id=bot.bot.id, level_side='s').order_by('level_queue')
    b_levels = OrderSmart.objects.filter(bot_id=bot.bot.id, level_side='b').order_by('level_queue')

    if len(s_levels) > 0:
        s_level = s_levels.first()
        if s_level.level_price <= bid:
            OrderSmart.objects.filter(id=s_level.id).update(level_price=0)

    if len(b_levels) > 0:
        b_level = b_levels.first()
        if b_level.level_price >= ask:
            OrderSmart.objects.filter(id=b_level.id).update(level_price=0)


    # for level in s_levels:
    #    print(level.level_queue, level.level_price)
    #
    # for level in b_levels:
    #     print(level.level_queue, level.level_price)

    # for level in levels:
    #     valueT = level.level_quantity - value
    #
    #     orders, order = filter_order(orders,
    #                                  level.order_id,
    #                                  level.side,
    #                                  level.level_price,
    #                                  valueT)
    #
    #     if order:
    #         print('OLD', order)
    #         OrderSmart.objects.filter(order_id=order.order_id).update(status=order.status, quantity=order.quantity)
    #
    #     else:
    #         if valueT > 0:
    #             if side == 'n' or side == 'b':
    #                 if level.level_side == 'b':
    #                     if level.level_price < ask and level.level_price < last and level.level_price < bid:
    #                         if level.level_side == 'b':
    #                             side = 'SIDE_BUY'
    #                         else:
    #                             side = 'SIDE_SELL'
    #                         order = bot.place_order(side, level.level_price, valueT)
    #                         if order:
    #                             print('NEW', order)
    #                             OrderSmart.objects.filter(id=level.id).update(
    #                                 order_id=order.order_id,
    #                                 status=order.status,
    #                                 order_type=order.order_type,
    #                                 side=order.side,
    #                                 limit_price=order.limit_price,
    #                                 quantity=order.quantity)
    #
    #
    #     if side == 'b' and value > 0:
    #         pater_levels = OrderSmart.objects.filter(pater_id=level.id)
    #         quantityP = 0
    #         for pater in pater_levels:
    #             quantityP += pater.level_quantity
    #             if value - quantityP > 0:
    #                 valueP = pater.level_quantity
    #             else:
    #                 valueP = value
    #
    #
    #
    #     for order in orders:
    #         if order.status == 'ORDER_STATUS_NEW' or order.status == 'ORDER_STATUS_PARTIALLY_FILLED':
    #             print('cancel_order', order)
    #             bot.cancel_order(order.order_id)
    #
    #



