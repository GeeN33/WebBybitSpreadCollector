from django.db import models
class InstrumentBinans(models.Model):
    symbol1 = models.CharField(max_length=100)
    symbol2 = models.CharField(max_length=100)
    is_updata = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.symbol1 + " " + self.symbol2
class BarSpreadBinans(models.Model):
    symbol = models.ForeignKey(InstrumentBinans, on_delete=models.CASCADE)
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


