from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .position import Position
    from .transaction import Transaction


class AssetClass(str, enum.Enum):
    STOCK = "STOCK"
    ETF = "ETF"
    CRYPTO = "CRYPTO"
    BOND = "BOND"
    CASH = "CASH"


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    asset_class: Mapped[AssetClass] = mapped_column(
        SAEnum(AssetClass, native_enum=False),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    exchange: Mapped[str | None] = mapped_column(String(50), nullable=True)

    transactions: Mapped[list[Transaction]] = relationship(
        "Transaction",
        back_populates="asset",
    )
    positions: Mapped[list[Position]] = relationship(
        "Position",
        back_populates="asset",
    )

    def __repr__(self) -> str:
        return f"<Asset id={self.id} ticker={self.ticker!r} class={self.asset_class}>"
