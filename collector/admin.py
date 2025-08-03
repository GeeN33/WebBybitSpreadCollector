from django.contrib import admin

from collector.models import Instrument, BarSpread

admin.site.register(Instrument)

admin.site.register(BarSpread)
