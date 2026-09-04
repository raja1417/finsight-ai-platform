from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.models import (
    Holding,
    Portfolio,
    PortfolioAnalytics,
    Transaction,
    TransactionCreate,
)


class PortfolioService:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    def get_portfolio(self, portfolio_id: str) -> Portfolio:
        holdings = [
            Holding(symbol="FINS", quantity=Decimal("10"), market_value=Decimal("1250.00"))
        ]
        return Portfolio(
            id=portfolio_id,
            as_of=date.today(),
            total_value=sum((holding.market_value for holding in holdings), Decimal()),
            holdings=holdings,
        )

    def list_transactions(self, portfolio_id: str) -> list[Transaction]:
        return [item for item in self._transactions if item.portfolio_id == portfolio_id]

    def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        stored = Transaction(
            id=str(uuid4()),
            **transaction.model_dump(),
        )
        self._transactions.append(stored)
        return stored

    def get_analytics(self, portfolio_id: str) -> PortfolioAnalytics:
        portfolio = self.get_portfolio(portfolio_id)
        return PortfolioAnalytics(
            portfolio_id=portfolio_id,
            total_value=portfolio.total_value,
            holding_count=len(portfolio.holdings),
            as_of=portfolio.as_of,
        )
