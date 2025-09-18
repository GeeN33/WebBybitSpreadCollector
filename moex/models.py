from django.db import models


class BotSpreadBollinger(models.Model):
    CHOICES_SIDE = (
        ('b', 'b'),
        ('s', 's'),
        ('n', 'n'),)
    name = models.CharField(max_length=100)
    secret_key = models.TextField()
    jwt_token = models.TextField()
    account_id = models.CharField(max_length=100)
    base_symbol = models.CharField(max_length=100)
    symbol1 = models.CharField(max_length=100)
    symbol2 = models.CharField(max_length=100)
    step_price = models.FloatField()
    lot_max  = models.IntegerField()
    lot_work  = models.IntegerField()
    side = models.CharField(help_text="side", max_length=3, choices=CHOICES_SIDE, default='n', null=True, blank=True)
    value  = models.FloatField(default=0, null=True, blank=True)
    ask = models.FloatField(default=0, null=True, blank=True)
    last = models.FloatField(default=0, null=True, blank=True)
    bid = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name
class BollingerLevel(models.Model):
    CHOICES_TYPE = (
        ('sma', 'sma'),
        ('high', 'high'),
        ('low', 'low'),)

    bot = models.ForeignKey(BotSpreadBollinger, on_delete=models.CASCADE)
    level_id = models.IntegerField(default=0, null=True, blank=True)
    level_high = models.IntegerField(default=0, null=True, blank=True)
    level_sma = models.IntegerField(default=0, null=True, blank=True)
    level_low = models.IntegerField(default=0, null=True, blank=True)
    level_work = models.BooleanField(default=False, null=True, blank=True)
    level_stop_high = models.BooleanField(default=False, null=True, blank=True)
    level_stop_low = models.BooleanField(default=False, null=True, blank=True)
    period = models.IntegerField(default=0, null=True, blank=True)
    deviation = models.FloatField(default=0, null=True, blank=True)
    level_type = models.CharField(help_text="bollinger type", max_length=30, choices=CHOICES_TYPE)
    level_price = models.FloatField(default=0, null=True, blank=True)
    normal_price = models.FloatField(default=0, null=True, blank=True)

    order_id = models.CharField(max_length=100, default='', null=True, blank=True)
    status = models.CharField(max_length=100, default='', null=True, blank=True)
    side = models.CharField(max_length=100, default='', null=True, blank=True)
    limit_price = models.FloatField(default=0, null=True, blank=True)
    quantity = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return (f'{self.level_id} | {self.level_high} | {self.level_low}'
                f' *** {self.bot.name} {self.level_type} {self.period} {self.deviation}'
                f' {self.level_price} *** {self.normal_price} *** {self.level_stop_low} _ {self.level_stop_high} ***'
                f' {self.normal_price} {self.quantity} {self.side}')

    class Meta:
        ordering = ('level_id',)