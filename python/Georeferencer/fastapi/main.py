from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
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
app.mount("/static", StaticFiles(directory="app/static"), name="static")
for router in all_routers:
    app.include_router(router)

async def favicon():
    return FileResponse("app/static/IMG/cenigaalogo.png", media_type="image/png")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon_redirect():
    return await favicon()

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    return FileResponse("app/static/HTML/index.html")