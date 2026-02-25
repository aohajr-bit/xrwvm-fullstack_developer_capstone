from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("register", views.registration, name="register"),
    path("get_dealers", views.get_dealerships, name="get_dealers"),
    path("get_cars", views.get_cars_view, name="get_cars"),
    path("add_review", views.add_review, name="add_review"),
]