from fastapi import FastAPI, Query, HTTPException, status
from typing import Optional
from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker
from .models import CryptoRankingAndPrice, MergedData
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

engine = create_engine(os.getenv("DB_URL"))
Session = sessionmaker(bind=engine)

@app.get("/crypto-price-and-rank/", response_model=MergedData)
async def get_merged_data(
    limit: int = Query(..., title="Limit", description="Number of top cryptocurrency to return"),
    datetime: Optional[str] = Query(None, title="Datetime", description="Timestamp in ISO format"),
    format: Optional[str] = Query("json", title="Format", description="Output format: json or csv")):
    
    if limit < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be greater than or equal to 0",
        )
    # Create a database session
    session = Session()

    # if datetime:
    #     query = session.query(CryptoRankingAndPrice).filter(CryptoRankingAndPrice.timestamp <= datetime).order_by(CryptoRankingAndPrice.timestamp.desc())
    # else:
    #     query = session.query(CryptoRankingAndPrice).order_by(CryptoRankingAndPrice.timestamp.desc())
    # query = query.order_by(CryptoRankingAndPrice.rank.asc()).limit(limit)
    # merged_data = query.all()

    if datetime:
        subquery = session.query(
            CryptoRankingAndPrice.symbol,
            func.max(CryptoRankingAndPrice.timestamp).label('max_timestamp')
        ).filter(
            CryptoRankingAndPrice.timestamp <= datetime
        ).group_by(
            CryptoRankingAndPrice.symbol
        ).subquery()
    else:
        subquery = session.query(
            CryptoRankingAndPrice.symbol,
            func.max(CryptoRankingAndPrice.timestamp).label('max_timestamp')
        ).group_by(
            CryptoRankingAndPrice.symbol
        ).subquery()

    query = session.query(CryptoRankingAndPrice).join(
        subquery,
        and_(
            CryptoRankingAndPrice.symbol == subquery.c.symbol,
            CryptoRankingAndPrice.timestamp == subquery.c.max_timestamp
        )
    ).order_by(
        CryptoRankingAndPrice.timestamp.desc(),
        CryptoRankingAndPrice.rank.asc()
    ).limit(limit)

    merged_data = query.all()
    session.close()
    if format == "json":
        merged_data = [
        {
            "symbol": data.symbol,
            "price_usd":data.price_usd,
            "rank":data.rank, 
        }
        for data in merged_data]
        return {"data": merged_data}

    elif format == "csv":
        csv_data = "\n".join([f"{data.symbol},{data.price_usd},{data.rank}" for data in merged_data])
        return {"data": csv_data}
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Supported formats: json, csv")
