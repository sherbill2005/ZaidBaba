from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.i),
    path('admin/', admin.site.urls),
    path('shop/', include("shop.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
