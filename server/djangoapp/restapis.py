import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode, quote

load_dotenv()

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url", default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    """
    Generic GET request helper to call the Node/Mongo backend.

    Examples:
      get_request("fetchDealers")
      get_request("fetchReviews", dealerId="15")
    """
    # Build query string safely (no trailing &)
    params = urlencode({k: v for k, v in kwargs.items()}) if kwargs else ""
    # Lab-style URL format: <backend_url><endpoint>?<params>
    # Ensure we don't end up with double slashes or missing slashes.
    base = backend_url.rstrip("/")
    ep = "/" + endpoint.lstrip("/")
    request_url = f"{base}{ep}"
    if params:
        request_url = f"{request_url}?{params}"

    print("GET from {} ".format(request_url))

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None


def analyze_review_sentiments(text):
    """
    Calls the sentiment analyzer microservice on Code Engine.

    Expected format:
      <sentiment_analyzer_url>/analyze/<text>
    """
    base = sentiment_analyzer_url.rstrip("/")
    safe_text = quote(text)  # handles spaces and special chars
    request_url = f"{base}/analyze/{safe_text}"
    print("Sentiment GET from {} ".format(request_url))

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None


def post_review(data_dict):
    """
    POST a review to the backend (will be used in later steps if required).
    Endpoint name may vary by lab version; adjust if your instructions say otherwise.
    """
    try:
        base = backend_url.rstrip("/")
        request_url = f"{base}/insert_review"
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None
