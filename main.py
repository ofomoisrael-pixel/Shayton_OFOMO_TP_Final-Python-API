from fastapi import FastAPI

from base_donnees import Base, engine
from routes import router, auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Médiathèque - Albums",
    version="1.0.0",
)

app.include_router(router)
app.include_router(auth_router)


@app.get("/")
def accueil():
    return {"message": "API opérationnelle"}