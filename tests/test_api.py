from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_creation_album():
    connexion = client.post(
        "/connexion",
        data={
            "username": "admin",
            "password": "admin123",
        },
    )

    assert connexion.status_code == 200

    token = connexion.json()["access_token"]

    response = client.post(
        "/albums",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "titre": "Discovery",
            "artiste": "Daft Punk",
            "genre": "electro",
            "annee": 2001,
            "note": 9.5,
        },
    )

    assert response.status_code == 201

    donnees = response.json()

    assert donnees["titre"] == "Discovery"
    assert donnees["artiste"] == "Daft Punk"
    assert donnees["genre"] == "electro"
    assert donnees["annee"] == 2001
    assert donnees["note"] == 9.5
    assert "secret_interne" not in donnees


def test_creation_sans_authentification():
    response = client.post(
        "/albums",
        json={
            "titre": "Random Access Memories",
            "artiste": "Daft Punk",
            "genre": "electro",
            "annee": 2013,
            "note": 9,
        },
    )

    assert response.status_code == 401