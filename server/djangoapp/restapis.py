import requests
import json
import os

NODE_BACKEND_URL = "http://localhost:3030"


def get_request(endpoint, **kwargs):
    url = f"{NODE_BACKEND_URL}{endpoint}"
    response = requests.get(url, params=kwargs, timeout=10)
    response.raise_for_status()
    return response.json()


def post_review(data_dict):
    url = f"{NODE_BACKEND_URL}/insert_review"
    response = requests.post(url, json=data_dict, timeout=10)
    response.raise_for_status()
    return response.json()


def analyze_review_sentiments(text):
    # Strict/simple local stub
    return {"sentiment": "neutral"}


def get_cars():
    car_file = "/home/project/xrwvm-fullstack_developer_capstone/server/database/data/car_records.json"

    if not os.path.exists(car_file):
        raise FileNotFoundError(f"Cars file not found: {car_file}")

    with open(car_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Accept common capstone formats
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        if "cars" in data and isinstance(data["cars"], list):
            return data["cars"]
        if "CarRecords" in data and isinstance(data["CarRecords"], list):
            return data["CarRecords"]

    raise Exception("Unexpected car_records.json format")