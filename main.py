from fastapi import FastAPI

from base_donnees import Base, engine
from routes import router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Médiathèque - Albums",
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def accueil():
    return {"message": "API opérationnelle"}