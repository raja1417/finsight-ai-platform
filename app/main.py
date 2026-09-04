from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, status

from app.config import Settings, get_settings
from app.models import Portfolio, PortfolioAnalytics, Transaction, TransactionCreate
from app.services import PortfolioService

app = FastAPI(title="FinSight AI Platform", version="1.0.0")


@lru_cache
def get_portfolio_service() -> PortfolioService:
    return PortfolioService(get_settings().database_url)


@app.get("/healthz", tags=["health"])
def health(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/portfolios/{portfolio_id}", response_model=Portfolio, tags=["portfolio"])
def get_portfolio(
    portfolio_id: str, portfolio_service: Annotated[PortfolioService, Depends(get_portfolio_service)]
) -> Portfolio:
    return portfolio_service.get_portfolio(portfolio_id)


@app.get("/portfolios/{portfolio_id}/transactions", response_model=list[Transaction], tags=["transactions"])
def list_transactions(
    portfolio_id: str, portfolio_service: Annotated[PortfolioService, Depends(get_portfolio_service)]
) -> list[Transaction]:
    return portfolio_service.list_transactions(portfolio_id)


@app.post(
    "/transactions",
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
    tags=["transactions"],
)
def create_transaction(
    transaction: TransactionCreate,
    portfolio_service: Annotated[PortfolioService, Depends(get_portfolio_service)],
) -> Transaction:
    return portfolio_service.create_transaction(transaction)


@app.get(
    "/portfolios/{portfolio_id}/analytics",
    response_model=PortfolioAnalytics,
    tags=["analytics"],
)
def get_analytics(
    portfolio_id: str, portfolio_service: Annotated[PortfolioService, Depends(get_portfolio_service)]
) -> PortfolioAnalytics:
    return portfolio_service.get_analytics(portfolio_id)
