from typing import List
from pydantic import BaseModel

class CryptoRank(BaseModel):
    rank: int
    symbol: str

class CryptoRankList(BaseModel):
    ranks: List[CryptoRank]
