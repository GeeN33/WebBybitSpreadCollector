from django.db import models

class BotGrid(models.Model):
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
