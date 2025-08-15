from django.db import models

class InstrumentGateio(models.Model):
    basis_rate = models.FloatField(default=0)
    cycle = models.CharField(max_length=20)
    settle_fee_rate = models.FloatField(default=0)
    in_delisting = models.BooleanField()
    expire_time = models.IntegerField()
    risk_limit_base = models.FloatField(default=0)
    index_price = models.FloatField(default=0)
    order_price_round = models.FloatField(default=0)
    order_size_min = models.IntegerField()
    ref_rebate_rate = models.FloatField(default=0)
    name = models.CharField(max_length=50)
    ref_discount_rate = models.FloatField(default=0)
    order_price_deviate = models.FloatField(default=0)
    maintenance_rate = models.FloatField(default=0)
    mark_type = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    basis_value = models.FloatField(default=0)
    leverage_min = models.FloatField(default=0)
    settle_price_interval = models.IntegerField()
    last_price = models.FloatField(default=0)
    mark_price = models.FloatField(default=0)
    order_size_max = models.IntegerField()
    maker_fee_rate = models.FloatField(default=0)
    settle_price_duration = models.IntegerField()
    config_change_time = models.IntegerField()
    orderbook_id = models.IntegerField()
    trade_size = models.IntegerField()
    underlying = models.CharField(max_length=50)
    position_size = models.IntegerField()
    orders_limit = models.IntegerField()
    quanto_multiplier = models.FloatField(default=0)
    basis_impact_value = models.FloatField(default=0)
    mark_price_round = models.FloatField(default=0)
    settle_price = models.FloatField(default=0)
    leverage_max = models.FloatField(default=0)
    risk_limit_max = models.IntegerField()
    taker_fee_rate = models.FloatField(default=0)
    trade_id = models.IntegerField()
    risk_limit_step = models.FloatField(default=0)
    is_updata = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PairGateio(models.Model):
    base_symbol = models.CharField(max_length=10)
    symbol1 = models.CharField(max_length=100)
    symbol2 = models.CharField(max_length=100)
    delivery1 = models.BooleanField(default=True)
    delivery2 = models.BooleanField(default=False)
    is_updata = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('symbol1', 'symbol2')

    def __str__(self):
        return self.base_symbol + ': ' + self.symbol1 + ' *** ' + self.symbol2

class BarSpreadGateio(models.Model):
    symbol = models.ForeignKey(PairGateio, on_delete=models.CASCADE)
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