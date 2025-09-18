


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