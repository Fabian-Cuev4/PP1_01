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
    # Inicializar MySQL primero (crea DB y tablas si no existen)
    # Usamos try-except para no bloquear el startup si hay problemas temporales
    try:
        MySQLConnection.inicializar_base_datos()
    except Exception as e:
        print(f"Advertencia: No se pudo inicializar MySQL en el startup: {e}")
        print("La aplicación continuará, pero algunas funciones pueden no estar disponibles.")
        print("MySQL se intentará inicializar automáticamente en el próximo request.")
    
    # Luego conectar MongoDB
    try:
        MongoDB.conectar()
    except Exception as e:
        print(f"Advertencia: No se pudo conectar a MongoDB en el startup: {e}")
        print("La aplicación continuará, pero algunas funciones pueden no estar disponibles.")
        print("MongoDB se intentará conectar automáticamente en el próximo request.")

@app.on_event("shutdown")
def shutdown_db_client():
    MongoDB.cerrar()

# Desde /app/main.py: parent = /app/
base_path = Path(__file__).resolve().parent


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