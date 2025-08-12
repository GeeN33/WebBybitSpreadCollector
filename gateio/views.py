from rest_framework.generics import ListAPIView

from gateio.models import BarSpreadGateio, PairGateio
from gateio.serializers import BarSpreadGateioSerializer, PairGateioSerializer


class GetBarSpreadGateioListAPIView(ListAPIView):
    serializer_class = BarSpreadGateioSerializer

    def get_queryset(self):
        symbol1 = self.request.query_params.get('symbol1', '')
        symbol2 = self.request.query_params.get('symbol2', '')
        return BarSpreadGateio.objects.filter(symbol__symbol1=symbol1, symbol__symbol2=symbol2)


class GetPairGateioListAPIView(ListAPIView):
    serializer_class = PairGateioSerializer

    def get_queryset(self):
        return PairGateio.objects.filter(is_active=True)



# http://localhost:8535/gateio/instrument/list/
# http://localhost:8535/gateio/collector/barspread/list/?format=json&symbol1=ADA_USDT_20250815&symbol2=ADA_USDT
