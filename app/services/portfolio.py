from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import DateTime, Numeric, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from app.models import (
    Holding,
    Portfolio,
    PortfolioAnalytics,
    Transaction,
    TransactionCreate,
)


class Base(DeclarativeBase):
    pass


class TransactionRecord(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    portfolio_id: Mapped[str] = mapped_column(String(64), index=True)
    symbol: Mapped[str | None] = mapped_column(String(10))
    transaction_type: Mapped[str] = mapped_column(String(16))
    quantity: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class PortfolioService:
    def __init__(self, database_url: str) -> None:
        connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
        self._engine = create_engine(database_url, connect_args=connect_args)
        Base.metadata.create_all(self._engine)

    def get_portfolio(self, portfolio_id: str) -> Portfolio:
        """Return sample holdings until market-data integration is configured."""
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
        with Session(self._engine) as session:
            records = session.scalars(
                select(TransactionRecord)
                .where(TransactionRecord.portfolio_id == portfolio_id)
                .order_by(TransactionRecord.occurred_at)
            ).all()
        return [
            Transaction(
                id=record.id,
                portfolio_id=record.portfolio_id,
                symbol=record.symbol,
                transaction_type=record.transaction_type,
                quantity=record.quantity,
                amount=record.amount,
                occurred_at=record.occurred_at,
            )
            for record in records
        ]

    def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        stored = Transaction(id=str(uuid4()), **transaction.model_dump())
        with Session(self._engine) as session:
            session.add(
                TransactionRecord(
                    id=stored.id,
                    portfolio_id=stored.portfolio_id,
                    symbol=stored.symbol,
                    transaction_type=stored.transaction_type.value,
                    quantity=stored.quantity,
                    amount=stored.amount,
                    occurred_at=stored.occurred_at,
                )
            )
            session.commit()
        return stored

    def get_analytics(self, portfolio_id: str) -> PortfolioAnalytics:
        portfolio = self.get_portfolio(portfolio_id)
        return PortfolioAnalytics(
            portfolio_id=portfolio_id,
            total_value=portfolio.total_value,
            holding_count=len(portfolio.holdings),
            as_of=portfolio.as_of,
        )
