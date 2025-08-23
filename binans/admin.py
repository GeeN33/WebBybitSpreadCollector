from django.contrib import admin

from binans.models import InstrumentBinans, BarSpreadBinans

admin.site.register(InstrumentBinans)


@admin.register(BarSpreadBinans)
class BarSpreadBinansAdmin(admin.ModelAdmin):
    model = BarSpreadBinans
    list_display = ('id', 'updated_at',)
