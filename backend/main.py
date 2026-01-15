# backend/main.py
from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from app.routes import views, maquina, mantenimiento # Importamos ambos

app = FastAPI()
base_path = Path(__file__).resolve().parent.parent

# Ahora buscamos frontend/static desde la raíz
app.mount(
    "/static", 
    StaticFiles(directory=base_path / "frontend" / "static"), 
    name="static"
)

app.include_router(views.route)    # Incluye las vistas
app.include_router(maquina.router) # Incluye las acciones maquina 
app.include_router(mantenimiento.router) ## Incluye las acciones mantenimiento