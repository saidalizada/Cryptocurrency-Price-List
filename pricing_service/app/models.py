from pydantic import BaseModel
from typing import List

class CryptoPrice(BaseModel):
    symbol: str
    price_usd: float

class CryptoPriceList(BaseModel):
    prices: List[CryptoPrice]
