import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_pricing_data(limit: int):
    async with httpx.AsyncClient() as client:
        pricing_service_url = os.getenv("PRICING_SERVICE_URL")
        response = await client.get(f"{pricing_service_url}")
        response.raise_for_status()
        return response.json()

async def get_ranking_data(limit: int):
    async with httpx.AsyncClient() as client:
        ranking_service_url = os.getenv("RANKING_SERVICE_URL")
        response = await client.get(f"{ranking_service_url}?limit={limit}")
        response.raise_for_status()
        return response.json()

