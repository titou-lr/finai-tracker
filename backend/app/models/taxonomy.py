from __future__ import annotations

import enum

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TaxonomyLevel(str, enum.Enum):
    ASSET_CLASS = "class"
    SECTOR = "sector"
    GEO = "geo"


class Taxonomy(Base):
    """Hierarchical taxonomy tree for asset classification (class / sector / geo)."""

    __tablename__ = "taxonomies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[TaxonomyLevel] = mapped_column(
        SAEnum(TaxonomyLevel, native_enum=False),
        nullable=False,
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("taxonomies.id"),
        nullable=True,
    )

    # Self-referential relationship — parent_id points to the root node when NULL
    children: Mapped[list[Taxonomy]] = relationship(
        "Taxonomy",
        back_populates="parent",
    )
    parent: Mapped[Taxonomy | None] = relationship(
        "Taxonomy",
        back_populates="children",
        remote_side="Taxonomy.id",
    )

    def __repr__(self) -> str:
        return f"<Taxonomy id={self.id} name={self.name!r} level={self.level}>"
