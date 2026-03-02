from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Root -> serve React shell (index.html)
    path("", views.root_redirect, name="root_redirect"),

    # Frontend page routes (React SPA shell)
    path("login", TemplateView.as_view(template_name="Home.html"), name="login_page"),
    path("register", TemplateView.as_view(template_name="Home.html"), name="register_page"),
    path("dealers", TemplateView.as_view(template_name="Home.html"), name="dealers_page"),
    path("dealer/<int:id>", TemplateView.as_view(template_name="Home.html"), name="dealer_page"),
    path("postreview/<int:id>", TemplateView.as_view(template_name="Home.html"), name="postreview_page"),
]