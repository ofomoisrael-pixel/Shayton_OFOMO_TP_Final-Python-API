from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth import (
    USERNAME,
    creer_token,
    mot_de_passe_hash,
    obtenir_utilisateur_connecte,
    verifier_mot_de_passe,
)
from base_donnees import get_db
from modeles import AlbumCreation, AlbumMiseAJour, AlbumSortie
from tables import Album


router = APIRouter(
    prefix="/albums",
    tags=["Albums"],
)

auth_router = APIRouter(
    tags=["Authentification"],
)


@auth_router.post("/connexion")
def connexion(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    if form_data.username != USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
        )

    if not verifier_mot_de_passe(
        form_data.password,
        mot_de_passe_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
        )

    token = creer_token(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post(
    "",
    response_model=AlbumSortie,
    status_code=status.HTTP_201_CREATED,
)
def creer_album(
    donnees: AlbumCreation,
    db: Session = Depends(get_db),
    utilisateur: str = Depends(obtenir_utilisateur_connecte),
):
    album = Album(
        titre=donnees.titre,
        artiste=donnees.artiste,
        genre=donnees.genre.value,
        annee=donnees.annee,
        note=donnees.note,
        secret_interne="donnee-secrete",
    )

    db.add(album)
    db.commit()
    db.refresh(album)

    return album


@router.get(
    "",
    response_model=list[AlbumSortie],
)
def lister_albums(
    db: Session = Depends(get_db),
):
    albums = db.scalars(
        select(Album)
    ).all()

    return albums


@router.get(
    "/{album_id}",
    response_model=AlbumSortie,
)
def obtenir_album(
    album_id: int,
    db: Session = Depends(get_db),
):
    album = db.get(Album, album_id)

    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album introuvable",
        )

    return album


@router.put(
    "/{album_id}",
    response_model=AlbumSortie,
)
def modifier_album(
    album_id: int,
    donnees: AlbumMiseAJour,
    db: Session = Depends(get_db),
    utilisateur: str = Depends(obtenir_utilisateur_connecte),
):
    album = db.get(Album, album_id)

    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album introuvable",
        )

    modifications = donnees.model_dump(
        exclude_unset=True
    )

    if "genre" in modifications:
        modifications["genre"] = modifications["genre"].value

    for champ, valeur in modifications.items():
        setattr(album, champ, valeur)

    db.commit()
    db.refresh(album)

    return album


@router.delete(
    "/{album_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def supprimer_album(
    album_id: int,
    db: Session = Depends(get_db),
    utilisateur: str = Depends(obtenir_utilisateur_connecte),
):
    album = db.get(Album, album_id)

    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album introuvable",
        )

    db.delete(album)
    db.commit()

    return None