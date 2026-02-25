from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend page routes (/login, /dealers, etc.)
    path('', include('djangoapp.urls')),

    # API routes (/djangoapp/login, /djangoapp/get_cars, etc.)
    path('djangoapp/', include('djangoapp.api_urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)