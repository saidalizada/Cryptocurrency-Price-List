from httpx import AsyncClient
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv
load_dotenv()


async def get_ranking_data(limit):
    if limit < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be greater than or equal to 0",
        )
    api_key = os.getenv("CRYPTOCOMPARE_API_KEY") 
    api_url = os.getenv("CRYPTOCOMPARE_API_URL") 
    url = f'{api_url}?limit={limit}&tsym=USD'

    headers = {'Apikey': api_key}

    async with AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get('Data', [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []
