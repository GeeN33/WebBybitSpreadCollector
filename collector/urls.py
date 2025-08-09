from django.urls import path

from collector.views import GetBarSpreadListAPIView

urlpatterns = [
    path('barspread/list/', GetBarSpreadListAPIView.as_view(), name='barspread-list'),]