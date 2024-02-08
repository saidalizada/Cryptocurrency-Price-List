from fastapi import FastAPI, Query, HTTPException, Depends
from .external_api import get_ranking_data
from .models import CryptoRankList
from cachetools import TTLCache

app = FastAPI()

ranking_cache = TTLCache(maxsize=1000, ttl=60)

async def get_cached_ranking_data(limit: int) -> list:
    if limit in ranking_cache:
        print("catching")
        return ranking_cache[limit]
    new_data = await get_ranking_data(limit)
    ranking_cache[limit] = new_data
    return new_data

@app.get("/crypto-ranks/", response_model=CryptoRankList)
async def get_crypto_ranks(limit: int = Query(default=10, description="Get the current ranking information")):
    try:
        # Use the cached data if available, otherwise fetch new data
        ranking_data = await get_cached_ranking_data(limit)
        ranks = []

        for i, crypto_data in enumerate(ranking_data):
            coin_info = crypto_data.get("CoinInfo", {})
            raw_data = crypto_data.get("RAW", {}).get("USD", {})
            display_data = crypto_data.get("DISPLAY", {}).get("USD", {})

            rank = i + 1
            symbol = coin_info.get("Name")
            price_usd = display_data.get("PRICE")

            if rank and symbol and price_usd:
                ranks.append({"rank": rank, "symbol": symbol, "price_usd": price_usd})

        return {"ranks": ranks}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
