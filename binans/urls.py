from django.urls import path

from binans.views import GetBinansBarSpreadListAPIView, GetInstrumentBinansListAPIView

urlpatterns = [
    path('collector/barspread/list/<str:symbol1>/<str:symbol2>/', GetBinansBarSpreadListAPIView.as_view(), name='binans-barspread-list'),
    path('instrument/list/', GetInstrumentBinansListAPIView.as_view(), name='instrument-list'),
]

