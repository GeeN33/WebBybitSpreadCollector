from django.db import models

from moex.models import BotAuth

class BotSmart(models.Model):
    CHOICES_SIDE = (
        ('b', 'b'),
        ('s', 's'),
        ('n', 'n'),)

    auth_bot = models.ForeignKey(BotAuth, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    base_symbol = models.CharField(max_length=100)
    symbol1 = models.CharField(max_length=100)
    symbol2 = models.CharField(max_length=100)
    bot_side = models.CharField(help_text="side", max_length=3, choices=CHOICES_SIDE, default='n')
    step_price = models.FloatField(default=0)
    value_max = models.FloatField(default=0, blank=True)
    range_price = models.FloatField(default=0, blank=True)
    is_active = models.BooleanField(default=False)

    side = models.CharField(help_text="side", max_length=3, choices=CHOICES_SIDE, default='n', null=True, blank=True)
    value  = models.FloatField(default=0, null=True, blank=True)
    ask = models.FloatField(default=0, null=True, blank=True)
    last = models.FloatField(default=0, null=True, blank=True)
    bid = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

class OrderSmart(models.Model):
    CHOICES_SIDE = (
        ('b', 'b'),
        ('s', 's'),)
    bot = models.ForeignKey(BotSmart, on_delete=models.CASCADE, null=True, blank=True)
    level_id = models.IntegerField(default=0, blank=True)
    level_queue = models.IntegerField(default=0, blank=True)

    level_price = models.FloatField(default=0, null=True, blank=True)
    level_side = models.CharField(help_text="side", max_length=30, choices=CHOICES_SIDE)
    level_quantity = models.FloatField(default=0, null=True, blank=True)

    order_id = models.CharField(max_length=100, default='', null=True, blank=True)
    status = models.CharField(max_length=100, default='', null=True, blank=True)
    order_type = models.CharField(max_length=100, default='', null=True, blank=True)
    side = models.CharField(max_length=100, default='', null=True, blank=True)
    limit_price = models.FloatField(default=0, null=True, blank=True)
    quantity = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        ordering = ('level_id',)
    def __str__(self):
        res = ''
        if self.level_id:
            res += str(self.level_id) + ' '

        if self.bot:
            res += self.bot.name + ' '

        if self.level_price:
            res += str(self.level_price) + ' '

        if self.level_quantity:
            res += str(self.level_quantity) + ' '

        if self.level_side:
            res += str(self.level_side)

        return res