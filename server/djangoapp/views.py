from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .models import CarMake, CarModel
from .populate import initiate

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Missing userName or password"}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})

        return JsonResponse({"userName": username, "status": "Unauthorized"}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        email = data.get("email", "")

        if not username or not password:
            return JsonResponse({"error": "Missing userName or password"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Already Registered"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_cars(request):
    # Safer to check CarModel count (ensures models exist, not just makes)
    count = CarModel.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    return JsonResponse({"CarModels": cars})
