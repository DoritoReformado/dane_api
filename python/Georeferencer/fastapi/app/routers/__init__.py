import pkgutil
import importlib
from fastapi import APIRouter

all_routers: list[APIRouter] = []

# Recorre todos los submódulos en este paquete (app.routers.*)
for module_info in pkgutil.iter_modules(__path__):
    module_name = module_info.name
    # ignora archivos especiales si quieres, por ej.: __init__, utils, etc.
    if module_name.startswith("_"):
        continue

    module = importlib.import_module(f"{__name__}.{module_name}")
    router = getattr(module, "router", None)
    if router:
        all_routers.append(router)