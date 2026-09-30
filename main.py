from fastapi import FastAPI

from base_donnees import Base, engine
from tables import Album

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Médiathèque - Albums")


@app.get("/")
def accueil():
    return {"message": "API opérationnelle"}