from typing import List, Optional

from moex.lib.modelsPy import Order


# def round_price(price, step):
#
#     size = str(step).split('.')
#
#     remainder = price % step
#     if remainder < step / 2:
#         return price - remainder
#     else:
#         return price + (step - remainder)


def round_price(price, step):

    remainder = int(price / step)

    rounded_price = remainder * step

    size = len(str(step).split('.')[-1])

    return round(rounded_price, size)

def filter_order(orders: List[Order],
                 order_id:str,
                 side:str,
                 limit_price:float,
                 quantity:float) -> ( List[Order],  Optional[Order]):

    for i, order in enumerate(orders):
        if order.order_id == order_id and order.side == side:
            if order.limit_price == limit_price  and order.order_type == 'ORDER_TYPE_LIMIT':
                if order.status == 'ORDER_STATUS_NEW' and order.quantity == quantity:
                    return orders, orders.pop(i)
                if order.status == 'ORDER_STATUS_PARTIALLY_FILLED':
                    return orders, orders.pop(i)

    return orders,  None
