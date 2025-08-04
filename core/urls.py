from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from core import settings

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='static/favicon.ico')),
    path('', RedirectView.as_view(url='admin/')),
    path('admin/', admin.site.urls),
    path('collector/', include('collector.urls')),
    path('binans/', include('binans.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
