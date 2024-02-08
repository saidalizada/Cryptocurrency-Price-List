from typing import List, Optional, Union
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP

Base = declarative_base()

class MergedDataItem(BaseModel):
    symbol: str
    price_usd: Optional[float]
    rank: int

class MergedDataJson(BaseModel):
    data: List[MergedDataItem]

class MergedDataCSV(BaseModel):
    data: str

MergedData = Union[MergedDataJson, MergedDataCSV]

class CryptoRankingAndPrice(Base):
    __tablename__ = 'crypto_ranking_and_price'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    price_usd = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)