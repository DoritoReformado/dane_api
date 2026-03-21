from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pkgutil
import importlib
from app.routers import all_routers

app = FastAPI(
    title="DANE-API",
    description="""
API para el consumo de informacion recompilada del DANE
""",
    version="0.1.0",
    contact={
        "name": "Carlos Vidal Gonzalez Lugo",
        "url": "https://www.cenigaa.org",
        "email": "carlos.vidal@cenigaa.onmicrosoft.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)
app.mount("/media", StaticFiles(directory="app/media"), name="media")
for router in all_routers:
    app.include_router(router)

@app.get("/")
def root():
    response = []
    for route in app.routes:
        response.append(f"{route.name}:{route.path}")


    return {
        "routes": response
    }