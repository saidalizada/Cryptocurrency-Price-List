from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .celeryconfig import app
from models.models import CryptoRankingAndPrice
from .get_info_from_api import get_price_data, get_ranking_data

load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
Session = sessionmaker(bind=engine)

@app.task
def collect_and_merge_data():
    session = Session()
    current_timestamp = datetime.utcnow()
    pricing_data = get_price_data()
    ranking_data = get_ranking_data()

    if pricing_data and ranking_data:
        pricing_by_symbol = {price["symbol"]: price["price_usd"] for price in pricing_data["prices"]} if pricing_data else {}
        merged_data = []
        for rank_info in ranking_data["ranks"]:
            symbol = rank_info["symbol"]
            price_usd = pricing_by_symbol.get(symbol)
            merged_data.append({
                "symbol": symbol,
                "price_usd": price_usd,
                "rank": rank_info["rank"],
                "timestamp": current_timestamp
            })
        existing_data = session.query(CryptoRankingAndPrice).filter_by(timestamp=current_timestamp).first()
        if existing_data:
            print("Data already exists for current timestamp.")
        else:
            session.bulk_insert_mappings(CryptoRankingAndPrice, merged_data)
            session.commit()
            print("Merged data collected and saved.")
    else:
        print("Failed to fetch price or ranking data.")
    session.close()