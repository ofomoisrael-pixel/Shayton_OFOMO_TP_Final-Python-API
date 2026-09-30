from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Genre(str, Enum):
    ROCK = "rock"
    POP = "pop"
    RAP = "rap"
    JAZZ = "jazz"
    CLASSIQUE = "classique"
    ELECTRO = "electro"


class AlbumCreation(BaseModel):
    titre: str = Field(min_length=1, max_length=200)
    artiste: str = Field(min_length=1, max_length=200)
    genre: Genre
    annee: int
    note: float = Field(ge=0, le=10)

    @field_validator("titre", "artiste")
    @classmethod
    def texte_non_vide(cls, valeur: str) -> str:
        valeur = valeur.strip()

        if not valeur:
            raise ValueError("Le texte ne peut pas être vide")

        return valeur

    @field_validator("annee")
    @classmethod
    def annee_valide(cls, valeur: int) -> int:
        annee_max = datetime.now().year

        if valeur < 1900 or valeur > annee_max:
            raise ValueError(
                f"L'année doit être comprise entre 1900 et {annee_max}"
            )

        return valeur


class AlbumMiseAJour(BaseModel):
    titre: str | None = Field(default=None, min_length=1, max_length=200)
    artiste: str | None = Field(default=None, min_length=1, max_length=200)
    genre: Genre | None = None
    annee: int | None = None
    note: float | None = Field(default=None, ge=0, le=10)

    @field_validator("titre", "artiste")
    @classmethod
    def texte_non_vide(cls, valeur: str | None) -> str | None:
        if valeur is None:
            return None

        valeur = valeur.strip()

        if not valeur:
            raise ValueError("Le texte ne peut pas être vide")

        return valeur

    @field_validator("annee")
    @classmethod
    def annee_valide(cls, valeur: int | None) -> int | None:
        if valeur is None:
            return None

        annee_max = datetime.now().year

        if valeur < 1900 or valeur > annee_max:
            raise ValueError(
                f"L'année doit être comprise entre 1900 et {annee_max}"
            )

        return valeur


class AlbumSortie(BaseModel):
    id: int
    titre: str
    artiste: str
    genre: Genre
    annee: int
    note: float

    model_config = {
        "from_attributes": True
    }


class AlbumAvecSecret(AlbumSortie):
    secret_interne: str