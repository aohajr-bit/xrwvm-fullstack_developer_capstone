import json
import os

import requests

NODE_BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:3030").rstrip("/")


def get_request(endpoint, **kwargs):
    url = NODE_BASE_URL + endpoint
    timeout = kwargs.pop("timeout", 10)
    resp = requests.get(url, timeout=timeout, **kwargs)
    resp.raise_for_status()
    return resp


def post_request(endpoint, payload, **kwargs):
    url = NODE_BASE_URL + endpoint
    timeout = kwargs.pop("timeout", 10)
    headers = {"Content-Type": "application/json"}
    resp = requests.post(
        url, headers=headers, json=payload, timeout=timeout, **kwargs
    )
    resp.raise_for_status()
    return resp


def _safe_json(resp):
    try:
        return resp.json()
    except Exception:
        return {}


def _normalize_dealers_payload(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        dealers = data.get("dealerships", [])
        return dealers if isinstance(dealers, list) else []
    return []


def _normalize_reviews_payload(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        reviews = data.get("reviews", [])
        return reviews if isinstance(reviews, list) else []
    return []


def get_dealers_from_db(state=""):
    if state:
        resp = get_request(f"/fetchDealers/{state}")
        data = _safe_json(resp)
        return _normalize_dealers_payload(data)

    resp = get_request("/fetchDealers")
    data = _safe_json(resp)
    return _normalize_dealers_payload(data)


def get_dealer_by_id_from_db(dealer_id):
    resp = get_request(f"/fetchDealer/{dealer_id}")
    data = _safe_json(resp)
    if isinstance(data, dict) and "dealership" in data:
        return data.get("dealership") or {}
    return data if isinstance(data, dict) else {}


def get_reviews_by_dealer_id_from_db(dealer_id):
    resp = get_request(f"/fetchReviews/dealer/{dealer_id}")
    data = _safe_json(resp)
    return _normalize_reviews_payload(data)


def post_review(review_json):
    return post_request("/insert_review", review_json)


def get_cars():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cars_path = os.path.join(base_dir, "database", "data", "car_records.json")

    if not os.path.exists(cars_path):
        raise FileNotFoundError(f"car_records.json not found at: {cars_path}")

    with open(cars_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cars = data.get("cars")
    if not isinstance(cars, list):
        raise ValueError("car_records.json must contain { 'cars': [ ... ] }")

    return cars


def analyze_review_sentiments(text):
    return "positive"