from fastapi import HTTPException, status
from httpx import AsyncClient
from datetime import datetime
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()


async def get_pricing_data(limit: int, timestamp: Optional[int] = None) -> dict:
    if limit < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be greater than or equal to 0",
        )
    api_key = os.getenv("COINMARKETCAP_API_KEY")  # Replace with your CoinMarketCap API key

    # Set the endpoint based on the presence of the timestamp
    endpoint = "historical" if timestamp else "latest"
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/{endpoint}"

    # Set parameters for the API request
    parameters = {
        'start': '1',
        'limit': str(limit),
        'convert': 'USD',
        
    }

    if timestamp:
        # Convert timestamp to ISO format
        iso_timestamp = datetime.utcfromtimestamp(timestamp).isoformat()
        parameters['time'] = iso_timestamp

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    async with AsyncClient() as client:
        try:
            # Make the API request asynchronously
            response = await client.get(url, headers=headers, params=parameters)
            response.raise_for_status()
            return response.json()
        except HTTPException as e:
            # Handle exceptions and raise a custom HTTPException
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
