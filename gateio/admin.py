from django.contrib import admin

from gateio.models import InstrumentGateio, PairGateio, BarSpreadGateio

admin.site.register(InstrumentGateio)

admin.site.register(PairGateio)

admin.site.register(BarSpreadGateio)


