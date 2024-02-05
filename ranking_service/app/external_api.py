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
    # Define the API endpoint
    api_key = os.getenv("CRYPTOCOMPARE_API_KEY") 
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit={limit}&tsym=USD'

    # Include your API key in the request headers
    headers = {'Apikey': api_key}

    # Make the asynchronous HTTP request
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract and return relevant information
        return data.get('Data', [])

    else:
        # Handle the error (you might want to raise an exception or return an error response)
        print(f"Error: {response.status_code}, {response.text}")
        return []
