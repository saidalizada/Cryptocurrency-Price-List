from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP

Base = declarative_base()

class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    price_usd = Column(Float, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

class Ranking(Base):
    __tablename__ = 'ranking'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    rank = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

class CryptoRankingAndPrice(Base):
    __tablename__ = 'crypto_ranking_and_price'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    price_usd = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
