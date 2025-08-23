from django.contrib import admin

from collector.models import Instrument, BarSpread

admin.site.register(Instrument)


@admin.register(BarSpread)
class BarSpreadBinansAdmin(admin.ModelAdmin):
    model = BarSpread
    list_display = ('id','symbol', 'updated_at',)
