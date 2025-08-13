from rest_framework.generics import ListAPIView

from collector.models import BarSpread
from collector.serializers import BarSpreadSerializer

class GetBarSpreadListAPIView(ListAPIView):
    serializer_class = BarSpreadSerializer

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol', '')
        return BarSpread.objects.filter(symbol__symbol=symbol).order_by('updated_at')
