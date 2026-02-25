import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .restapis import analyze_review_sentiments, get_cars, get_request, post_review


def root_redirect(request):
    return redirect("/login")


def registration(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST required"}, status=405)

    username = request.POST.get("username")
    password = request.POST.get("password")
    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")

    if not username or not password:
        return JsonResponse({"message": "Username and password are required."}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"message": "Username already exists."}, status=409)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    login(request, user)
    return JsonResponse({"userName": user.username, "status": 200})


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST required"}, status=405)

    try:
        content_type = request.content_type or ""

        if "application/json" in content_type:
            body = json.loads(request.body.decode("utf-8")) if request.body else {}
            username = body.get("username")
            password = body.get("password")
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")

        if not username or not password:
            return JsonResponse({"message": "Username and password are required", "status": 400}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return JsonResponse({"message": "Invalid credentials", "status": 401}, status=401)

        login(request, user)
        full_name = f"{user.first_name} {user.last_name}".strip()

        return JsonResponse({
            "userName": user.username,
            "fullName": full_name if full_name else user.username,
            "status": 200
        })
    except Exception as e:
        print("login_user error:", e)
        return JsonResponse({"message": str(e), "status": 500}, status=500)


def logout_request(request):
    logout(request)
    return JsonResponse({"status": 200, "message": "Logged out"})


def get_dealerships(request):
    try:
        dealers = get_request("/fetchDealers")

        if isinstance(dealers, dict) and "dealers" in dealers:
            return JsonResponse(dealers, safe=False)

        if isinstance(dealers, list):
            return JsonResponse({"dealers": dealers}, safe=False)

        return JsonResponse(
            {"message": "Unexpected dealers response shape", "data": dealers},
            status=500
        )
    except Exception as e:
        print("get_dealerships error:", e)
        return JsonResponse({"message": str(e)}, status=500)


def get_cars_view(request):
    try:
        cars = get_cars()

        if isinstance(cars, dict) and "cars" in cars:
            return JsonResponse(cars["cars"], safe=False)

        if isinstance(cars, list):
            return JsonResponse(cars, safe=False)

        return JsonResponse(
            {"message": "Unexpected cars response shape", "data": cars},
            status=500
        )
    except Exception as e:
        print("get_cars_view error:", e)
        return JsonResponse({"message": str(e)}, status=500)


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST required", "status": 405}, status=405)

    try:
        content_type = request.content_type or ""

        if "application/json" in content_type:
            data = json.loads(request.body.decode("utf-8")) if request.body else {}
        else:
            data = request.POST.dict()

        dealer_id = data.get("dealer_id")
        review_text = data.get("review")
        purchase = data.get("purchase", False)
        purchase_date = data.get("purchase_date", "")
        car = data.get("car", "")
        name = data.get("name")

        if dealer_id in [None, ""]:
            return JsonResponse({"message": "dealer_id is required", "status": 400}, status=400)

        if not name:
            return JsonResponse({"message": "Reviewer name is required", "status": 400}, status=400)

        if not review_text:
            return JsonResponse({"message": "Review text is required", "status": 400}, status=400)

        if isinstance(purchase, str):
            purchase = purchase.lower() in ["true", "1", "yes", "on"]

        sentiment_data = analyze_review_sentiments(review_text)
        sentiment = sentiment_data.get("sentiment", "neutral")

        outbound_review = {
            "dealership": int(dealer_id),
            "name": name,
            "review": review_text,
            "purchase": purchase,
            "purchase_date": purchase_date,
            "car": car,
            "sentiment": sentiment,
            "time": datetime.now().strftime("%Y-%m-%d")
        }

        backend_resp = post_review(outbound_review)

        return JsonResponse({
            "status": 200,
            "message": "Review added successfully",
            "backend_response": backend_resp
        })
    except ValueError as e:
        print("add_review value error:", e)
        return JsonResponse({"message": f"Invalid dealer_id: {e}", "status": 400}, status=400)
    except Exception as e:
        print("add_review error:", e)
        return JsonResponse({"message": str(e), "status": 500}, status=500)