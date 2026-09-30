from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from base_donnees import Base


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    titre: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    artiste: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    genre: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    annee: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    note: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    secret_interne: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="interne",
    )