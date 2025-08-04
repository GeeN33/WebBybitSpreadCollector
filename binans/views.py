from rest_framework.generics import ListAPIView

from binans.models import BarSpreadBinans, InstrumentBinans
from binans.serializers import BarSpreadBinansSerializer, InstrumentBinansSerializer


class GetBinansBarSpreadListAPIView(ListAPIView):
    serializer_class = BarSpreadBinansSerializer

    def get_queryset(self):
        symbol1 = self.kwargs.get('symbol1')
        symbol2 = self.kwargs.get('symbol2')
        return BarSpreadBinans.objects.filter(symbol__symbol1=symbol1, symbol__symbol2=symbol2)


class GetInstrumentBinansListAPIView(ListAPIView):
    serializer_class = InstrumentBinansSerializer

    def get_queryset(self):
        return InstrumentBinans.objects.filter(is_active=True)


# http://localhost:8535/binans/instrument/list/
# http://localhost:8535/binans/collector/barspread/list/BTCUSDT_250926/BTCUSDT/