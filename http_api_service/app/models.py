from typing import List, Optional
from pydantic import BaseModel

class MergedDataItem(BaseModel):
    symbol: str
    price_usd: Optional[float]
    rank: int

class MergedData(BaseModel):
    merged_data: List[MergedDataItem]
