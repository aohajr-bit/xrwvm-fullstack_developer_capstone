# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import logging
import json
# from .populate import initiate

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
    logout(request)  # Terminate user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)
