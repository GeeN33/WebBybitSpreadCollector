from django.db import models

class Instrument(models.Model):
    symbol = models.CharField(max_length=100, unique=True)
    contract_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    base_coin = models.CharField(max_length=10)
    quote_coin = models.CharField(max_length=10)
    settle_coin = models.CharField(max_length=10)
    tick_size = models.FloatField()
    min_price = models.FloatField()
    max_price = models.FloatField()
    lot_size = models.FloatField()
    min_size = models.FloatField()
    max_size = models.FloatField()
    launch_time = models.BigIntegerField()
    delivery_time = models.BigIntegerField()
    legs = models.JSONField(default=list)
    is_updata = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.symbol

class BarSpread(models.Model):
    symbol = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    per = models.CharField(max_length=10)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    last1 = models.FloatField(default=0, null=True)
    last2 = models.FloatField(default=0, null=True)
    funding = models.FloatField(default=0, null=True)
    fair1 = models.FloatField(default=0, null=True)
    fair2 = models.FloatField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol.symbol


