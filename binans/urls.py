from django.urls import path

from binans.views import GetBinansBarSpreadListAPIView, GetInstrumentBinansListAPIView

urlpatterns = [
    path('collector/barspread/list/', GetBinansBarSpreadListAPIView.as_view(), name='binans-barspread-list'),
    path('instrument/list/', GetInstrumentBinansListAPIView.as_view(), name='instrument-list'),
]

