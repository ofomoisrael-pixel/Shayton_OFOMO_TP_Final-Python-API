from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash


SECRET_KEY = "cle-tres-secrete-pour-le-tp"
ALGORITHM = "HS256"
DUREE_TOKEN_MINUTES = 30

USERNAME = "admin"
PASSWORD = "admin123"

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/connexion")

mot_de_passe_hash = password_hash.hash(PASSWORD)


def verifier_mot_de_passe(
    mot_de_passe: str,
    mot_de_passe_hash: str,
) -> bool:
    return password_hash.verify(
        mot_de_passe,
        mot_de_passe_hash,
    )


def creer_token(username: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=DUREE_TOKEN_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def obtenir_utilisateur_connecte(
    token: str = Depends(oauth2_scheme),
) -> str:
    erreur = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentification requise",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

        if username != USERNAME:
            raise erreur

        return username

    except jwt.PyJWTError:
        raise erreur