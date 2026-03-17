from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("kry-admin/", admin.site.urls),  # security: non-default admin URL reduces automated brute-force
    path("", include("main.urls")),
    path("services/", include("store.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
