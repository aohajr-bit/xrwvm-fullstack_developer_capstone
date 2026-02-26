from django.urls import path
from . import views

app_name = "djangoapp"

urlpatterns = [
    # Auth
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.registration, name="register"),

    # Dealers (BOTH with and without trailing slash)
    path("get_dealers", views.get_dealers, name="get_dealers_noslash"),
    path("get_dealers/", views.get_dealers, name="get_dealers"),

    path("get_dealers/<str:state>", views.get_dealers_by_state, name="get_dealers_by_state_noslash"),
    path("get_dealers/<str:state>/", views.get_dealers_by_state, name="get_dealers_by_state"),

    # Dealer + reviews
    path("get_dealer/<int:dealer_id>", views.get_dealer_details, name="get_dealer_details_noslash"),
    path("get_dealer/<int:dealer_id>/", views.get_dealer_details, name="get_dealer_details"),

    path("get_reviews/<int:dealer_id>", views.get_dealer_reviews, name="get_dealer_reviews_noslash"),
    path("get_reviews/<int:dealer_id>/", views.get_dealer_reviews, name="get_dealer_reviews"),

    # Add review
    path("add_review", views.add_review, name="add_review"),
    path("add_review/", views.add_review, name="add_review_slash"),

    # Cars
    path("get_cars", views.get_cars, name="get_cars_noslash"),
    path("get_cars/", views.get_cars, name="get_cars"),
]