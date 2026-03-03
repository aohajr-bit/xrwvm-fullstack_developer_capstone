from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Frontend page routes (/login, /dealers, /dealer/<id>, /postreview/<id>)
    path("", include("djangoapp.urls")),

    # API routes (/djangoapp/login, /djangoapp/get_cars, /djangoapp/add_review, etc.)
    path("djangoapp/", include("djangoapp.api_urls")),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
)
