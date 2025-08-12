from django.urls import path

from gateio.views import GetBarSpreadGateioListAPIView, GetPairGateioListAPIView

urlpatterns = [
    path('collector/barspread/list/', GetBarSpreadGateioListAPIView.as_view(), name='gateio-barspread-list'),
    path('instrument/list/', GetPairGateioListAPIView.as_view(), name='gateio-instrument-list'),
]

