from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
import requests

from .restapis import (
    get_dealers_from_db,
    get_dealer_by_id_from_db,
    get_reviews_by_dealer_id_from_db,
    post_review,
    analyze_review_sentiments,
    get_cars as rest_get_cars,
)

# ----------------------------
# React SPA shell
# ----------------------------
def root_redirect(request):
    # Serve the React shell (Home.html) at /
    return render(request, "Home.html")


def registration(request):
    context = {}
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = (request.POST.get("password") or "").strip()
        firstname = (request.POST.get("firstname") or "").strip()
        lastname = (request.POST.get("lastname") or "").strip()

        if not username or not password:
            context["error"] = "Username and password are required."
            return render(request, "registration.html", context)

        if User.objects.filter(username=username).exists():
            context["error"] = "Username already exists."
            return render(request, "registration.html", context)

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=firstname,
            last_name=lastname
        )
        user.save()
        return redirect("djangoapp:login")

    return render(request, "registration.html", context)


def login_user(request):
    if request.method == "GET":
        return render(request, "login.html")

    username = ""
    password = ""

    try:
        if request.body:
            data = json.loads(request.body.decode("utf-8"))
            username = (data.get("username") or "").strip()
            password = (data.get("password") or "").strip()
    except Exception:
        pass

    if not username:
        username = (request.POST.get("username") or "").strip()
    if not password:
        password = (request.POST.get("password") or "").strip()

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse(
            {
                "status": 200,
                "userName": user.username,
                "firstName": user.first_name,
                "lastName": user.last_name,
            }
        )

    return JsonResponse({"status": 401, "message": "Invalid credentials"}, status=401)


def logout_user(request):
    logout(request)
    return redirect("djangoapp:login")


def logout_request(request):
    return logout_user(request)


def get_dealers(request):
    dealers = get_dealers_from_db("")
    return JsonResponse({"status": 200, "dealers": dealers}, safe=False)


def get_dealers_by_state(request, state):
    if state.lower() == "all":
        dealers = get_dealers_from_db("")
    else:
        dealers = get_dealers_from_db(state)
    return JsonResponse({"status": 200, "dealers": dealers}, safe=False)


def get_dealer_details(request, dealer_id):
    dealer = get_dealer_by_id_from_db(dealer_id)
    return JsonResponse(dealer, safe=False)


def get_dealer_reviews(request, dealer_id):
    """
    Return a shape that satisfies multiple frontend expectations:
    - { reviews: [...] }  (what you confirmed)
    - { status: 200, reviews: [...] }  (common)
    - { status: 200, results: [...], data: [...], dealers: [...] } (defensive)
    """
    reviews = get_reviews_by_dealer_id_from_db(dealer_id)
    return JsonResponse(
        {
            "status": 200,
            "reviews": reviews,
            "results": reviews,
            "data": reviews,
        },
        safe=False
    )


def get_cars(request):
    cars = rest_get_cars()
    return JsonResponse(cars, safe=False)


def _next_review_id_for_dealer(dealer_id: int) -> int:
    try:
        existing = get_reviews_by_dealer_id_from_db(dealer_id)
        ids = []
        for r in existing:
            rid = r.get("id")
            if isinstance(rid, int):
                ids.append(rid)
            elif isinstance(rid, str) and rid.isdigit():
                ids.append(int(rid))
        return (max(ids) + 1) if ids else 1
    except Exception:
        return 1


def _parse_car_fields(car_value: str):
    if not car_value or not isinstance(car_value, str):
        return None, None, None
    parts = car_value.strip().split()
    if len(parts) < 3:
        return None, None, None
    year_part = parts[-1]
    if not year_part.isdigit():
        return None, None, None
    year_int = int(year_part)
    make = parts[0]
    model = " ".join(parts[1:-1])
    return make, model, year_int


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)

    payload = {}
    try:
        if request.body:
            payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        payload = {}

    if not payload:
        payload = request.POST.dict()

    dealer_id = payload.get("dealer_id")
    if dealer_id is None and "dealership" in payload:
        dealer_id = payload.get("dealership")

    try:
        dealer_id_int = int(dealer_id)
    except Exception:
        return JsonResponse({"status": 400, "message": "Invalid dealer_id"}, status=400)

    payload["dealership"] = dealer_id_int
    payload["id"] = _next_review_id_for_dealer(dealer_id_int)

    purchase_date = (payload.get("purchase_date") or "").strip()
    if not purchase_date:
        purchase_date = date.today().isoformat()
    payload["purchase_date"] = purchase_date

    purchase_val = payload.get("purchase", False)
    if isinstance(purchase_val, str):
        purchase_val = purchase_val.strip().lower() in ("true", "1", "yes", "y", "on")
    payload["purchase"] = bool(purchase_val)

    reviewer = payload.get("name")
    if reviewer is None or str(reviewer).strip() == "":
        payload["name"] = "Anonymous User"

    car_value = payload.get("car", "")
    car_make, car_model, car_year = _parse_car_fields(car_value)

    if car_make is None:
        cars = rest_get_cars()
        if not cars or not isinstance(cars, list):
            return JsonResponse({"status": 500, "message": "Cars list unavailable"}, status=500)
        first = cars[0]
        car_make = first.get("make")
        car_model = first.get("model")
        car_year = first.get("year")

    payload["car_make"] = car_make
    payload["car_model"] = car_model
    payload["car_year"] = int(car_year)

    review_text = payload.get("review", "")
    payload["sentiment"] = analyze_review_sentiments(review_text) if review_text else "neutral"

    if "dealer_id" in payload:
        del payload["dealer_id"]

    try:
        resp = post_review(payload)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"status": 500, "message": f"Node request failed: {str(e)}"}, status=500)

    try:
        data = resp.json()
    except Exception:
        text = getattr(resp, "text", "")
        data = {"status": resp.status_code, "message": text[:500]}

    if isinstance(data, dict) and "status" not in data:
        data["status"] = resp.status_code

    return JsonResponse(data, safe=False, status=resp.status_code)


def get_dealers_list(request):
    return get_dealers(request)


def get_dealer(request, dealer_id):
    return get_dealer_details(request, dealer_id)


def get_reviews(request, dealer_id):
    return get_dealer_reviews(request, dealer_id)


def add_review_to_db(request):
    return add_review(request)