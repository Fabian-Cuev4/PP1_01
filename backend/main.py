# backend/main.py
from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from app.routes import views, maquina, mantenimiento # Importamos ambos
from app.database.mongodb import MongoDB
from app.database.mysql import MySQLConnection

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    MongoDB.conectar()

@app.on_event("shutdown")
def shutdown_db_client():
    MongoDB.cerrar()

MySQLConnection.inicializar_base_datos()

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