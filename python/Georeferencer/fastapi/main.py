from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users as users_router

# Crea las tablas si no existen (en producción es mejor usar Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router.router)


@app.get("/")
def read_root():
    return {"message": "Hola FastAPI con PostgreSQL"}