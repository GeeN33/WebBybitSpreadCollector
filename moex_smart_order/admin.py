from django.contrib import admin

from moex_smart_order.models import OrderSmart, BotSmart

@admin.register(OrderSmart)
class OrderSmartAdmin(admin.ModelAdmin):
    model = OrderSmart
    list_filter = [
        'bot',
    ]



class OrderSmartInLine(admin.StackedInline):
    model = OrderSmart
    extra = 0


@admin.register(BotSmart)
class BotSmartAdmin(admin.ModelAdmin):
    model = BotSmart
    inlines = [OrderSmartInLine, ]



