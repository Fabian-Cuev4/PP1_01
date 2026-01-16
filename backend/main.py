# backend/main.py
from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from app.routes import views, maquina, mantenimiento, auth 
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


app.mount(
    "/static", 
    StaticFiles(directory=base_path / "frontend" / "static"), 
    name="static"
)

app.mount(
    "/templates", 
    StaticFiles(directory=base_path / "frontend" / "templates"), 
    name="templates"
)

app.include_router(views.route)  
app.include_router(maquina.router)  
app.include_router(mantenimiento.router) 
app.include_router(auth.router)