from rest_framework.generics import ListAPIView

from binans.models import BarSpreadBinans, InstrumentBinans
from binans.serializers import BarSpreadBinansSerializer, InstrumentBinansSerializer


class GetBinansBarSpreadListAPIView(ListAPIView):
    serializer_class = BarSpreadBinansSerializer

    def get_queryset(self):
        symbol1 = self.request.query_params.get('symbol1', '')
        symbol2 = self.request.query_params.get('symbol2', '')
        return BarSpreadBinans.objects.filter(symbol__symbol1=symbol1, symbol__symbol2=symbol2).order_by('updated_at')


class GetInstrumentBinansListAPIView(ListAPIView):
    serializer_class = InstrumentBinansSerializer

    def get_queryset(self):
        return InstrumentBinans.objects.filter(is_active=True)


# http://localhost:8535/binans/instrument/list/
# http://localhost:8535/binans/collector/barspread/list/?format=json&symbol1=BTCUSDT_250627&symbol2=BTCUSDT
# http://147.45.212.47:8535/binans/collector/barspread/list/?format=json&symbol1=BTCUSDT_250627&symbol2=BTCUSDT