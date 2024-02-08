import requests
import os
from dotenv import load_dotenv
load_dotenv()

pricing_service_url = os.getenv("PRICING_SERVICE_URL")
ranking_service_url = os.getenv("RANKING_SERVICE_URL")
max_items_per_request = os.getenv("MAX_ITEMS_PER_REQUEST")

def get_price_data():
    response = requests.get(f"{pricing_service_url}?limit={max_items_per_request}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_ranking_data():
    response = requests.get(f"{ranking_service_url}?limit{max_items_per_request}")
    if response.status_code == 200:
        return response.json()
    else:
        return None