from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from .external_api import get_pricing_data, get_ranking_data
from .models import MergedData

app = FastAPI()

@app.get("/merged-data/", response_model=MergedData)
async def get_merged_data(
    limit: int = Query(..., title="Limit", description="Number of results to return"),
    datetime: Optional[str] = Query(None, title="Datetime", description="Timestamp in ISO format"),
    format: Optional[str] = Query("json", title="Format", description="Output format: json or csv")
):
    # Get data from Pricing and Ranking services
    pricing_data = await get_pricing_data(limit)
    ranking_data = await get_ranking_data(limit)
    print(pricing_data)
    print(ranking_data)
    # Merge data based on cryptocurrency symbol (sample merge logic)
    merged_data = []
    merged_data = [
    {
        "symbol": p["symbol"],
        "price_usd": next((r["price_usd"] for r in pricing_data['prices'] if r["symbol"] == p["symbol"]), None),
        "rank": p["rank"]
    }
    for p in ranking_data['ranks']
]


    # Format data based on the requested format
    if format == "json":
        return {"merged_data": merged_data}
    elif format == "csv":
        csv_data = "\n".join([f"{item['symbol']},{item['price_usd']},{item['rank']}" for item in merged_data])
        return {"csv_data": csv_data}
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Supported formats: json, csv")
