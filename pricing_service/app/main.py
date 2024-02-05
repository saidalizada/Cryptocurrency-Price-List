from fastapi import FastAPI, Query, HTTPException
from .external_api import get_pricing_data
from .models import CryptoPriceList
from cachetools import TTLCache


app = FastAPI()

prices_cache = TTLCache(maxsize=1000, ttl=60)

async def get_cached_pricing_data(limit: int, timestamp: int) -> dict:
    key = (limit, timestamp)
    if key in prices_cache:
        print("catching")
        return prices_cache[key]
    new_data = await get_pricing_data(limit, timestamp)
    prices_cache[key] = new_data
    return new_data

@app.get("/crypto-prices/", response_model=CryptoPriceList)
async def get_crypto_prices(limit: int = Query(default=10, description="Number of results to return"), timestamp: int = None):
    try:
        # Use the cached data if available, otherwise fetch new data
        pricing_data = await get_cached_pricing_data(limit, timestamp)
        prices_list = []

        for crypto in pricing_data.get("data", []):
            symbol = crypto.get("symbol")
            price_usd = crypto.get("quote", {}).get("USD", {}).get("price")

            if symbol and price_usd:
                prices_list.append({"symbol": symbol, "price_usd": price_usd})

        return {"prices": prices_list}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
