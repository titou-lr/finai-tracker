from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .account import Account
    from .asset import Asset


class Position(Base):
    """Aggregated view of holdings per (account, asset) pair."""

    __tablename__ = "positions"
    __table_args__ = (
        UniqueConstraint("account_id", "asset_id", name="uq_positions_account_asset"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    avg_price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    account: Mapped[Account] = relationship("Account", back_populates="positions")
    asset: Mapped[Asset] = relationship("Asset", back_populates="positions")

    def __repr__(self) -> str:
        return (
            f"<Position id={self.id} account_id={self.account_id}"
            f" asset_id={self.asset_id} qty={self.quantity}>"
        )
