from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/administrateurs/', include('apps.administrateurs.urls')),
    path('api/tables/', include('apps.tables.urls')),
    path('api/menu/', include('apps.menu.urls')),
    path('api/commandes/', include('apps.commandes.urls')),
    path('api/alertes/', include('apps.alertes.urls')),
    path('api/services/', include('services.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
