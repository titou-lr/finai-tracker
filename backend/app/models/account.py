from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .position import Position
    from .transaction import Transaction


class AccountType(str, enum.Enum):
    CTO = "CTO"
    PEA = "PEA"
    CRYPTO = "CRYPTO"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[AccountType] = mapped_column(
        SAEnum(AccountType, native_enum=False),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    transactions: Mapped[list[Transaction]] = relationship(
        "Transaction",
        back_populates="account",
        cascade="all, delete-orphan",
    )
    positions: Mapped[list[Position]] = relationship(
        "Position",
        back_populates="account",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Account id={self.id} name={self.name!r} type={self.type}>"
