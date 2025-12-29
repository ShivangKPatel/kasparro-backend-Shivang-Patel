from sqlalchemy import Column, Integer, String, Numeric, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
from datetime import datetime

Base = declarative_base()

class RawData(Base):
    __tablename__ = "raw_data"
    id = Column(Integer, primary_key=True)
    source = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Coin(Base):
    __tablename__ = "coins"
    id = Column(Integer, primary_key=True)
    canonical_id = Column(String, nullable=False)
    symbol = Column(String)
    name = Column(String)
    price_usd = Column(Numeric)
    market_cap_usd = Column(Numeric)
    volume_24h_usd = Column(Numeric)
    source = Column(String)
    last_updated = Column(DateTime)
    __table_args__ = (UniqueConstraint('canonical_id', name='uq_coins_canonical_id'),)

class Checkpoint(Base):
    __tablename__ = "checkpoints"
    source = Column(String, primary_key=True)
    cursor = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)
