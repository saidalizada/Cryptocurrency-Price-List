from fastapi import HTTPException, status
from httpx import AsyncClient
from datetime import datetime
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()


async def get_pricing_data(limit: int) -> dict:
    if limit < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be greater than or equal to 0",
        )
    api_key = os.getenv("COINMARKETCAP_API_KEY")
    url = os.getenv("COINMARKETCAP_API_URL")

    parameters = {
        'start': '1',
        'limit': str(limit),
        'convert': 'USD',
        }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    async with AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=parameters)
            response.raise_for_status()
            return response.json()
        except HTTPException as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
