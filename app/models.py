from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class Holding(BaseModel):
    symbol: str = Field(pattern=r"^[A-Z0-9.-]{1,10}$")
    quantity: Decimal = Field(gt=0)
    market_value: Decimal = Field(ge=0)


class Portfolio(BaseModel):
    id: str
    as_of: date
    total_value: Decimal = Field(ge=0)
    holdings: list[Holding]


class TransactionCreate(BaseModel):
    portfolio_id: str = Field(min_length=1, max_length=64)
    symbol: str | None = Field(default=None, pattern=r"^[A-Z0-9.-]{1,10}$")
    transaction_type: TransactionType
    quantity: Decimal | None = Field(default=None, gt=0)
    amount: Decimal = Field(gt=0)
    occurred_at: datetime


class Transaction(TransactionCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)


class PortfolioAnalytics(BaseModel):
    portfolio_id: str
    total_value: Decimal = Field(ge=0)
    holding_count: int = Field(ge=0)
    as_of: date
