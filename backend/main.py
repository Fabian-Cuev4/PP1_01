# Este es el archivo principal que arranca todo el servidor (Backend)
# Aquí configuramos FastAPI, las bases de datos y las rutas de la web.

from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles
# Importamos las rutas que hemos creado en otros archivos
from app.routes import views, maquina, mantenimiento, auth 
from app.database.mongodb import MongoDB
from app.database.mysql import MySQLConnection

# Creamos la instancia principal de la aplicación FastAPI
app = FastAPI()

# Este evento se ejecuta justo cuando el servidor se enciende (Startup)
@app.on_event("startup")
def startup_db_client():
    
    #Función que inicializa las conexiones a las bases de datos al arrancar.
    # Intentamos inicializar MySQL (crear la base de datos y las tablas)
    try:
        # Llama a la función que crea todo en MySQL si no existe
        MySQLConnection.inicializar_base_datos()
    except Exception as e:
        # Si falla (por ejemplo, el motor no está listo), mostramos un aviso pero no detenemos el servidor
        print(f"Advertencia: No se pudo inicializar MySQL en el startup: {e}")
        print("La aplicación continuará intentándolo más tarde.")
    
    # Intentamos conectar con MongoDB para los logs y otros datos no relacionales
    try:
        MongoDB.conectar()
    except Exception as e:
        print(f"Advertencia: No se pudo conectar a MongoDB en el startup: {e}")

# Este evento se ejecuta cuando apagamos el servidor
@app.on_event("shutdown")
def shutdown_db_client():
    
    #erramos las conexiones de forma segura al apagar.
    MongoDB.cerrar()

# Obtenemos la ruta de este archivo para saber dónde están las carpetas de fotos, CSS y HTML
base_path = Path(__file__).resolve().parent

# "Montamos" la carpeta static para que el navegador pueda bajar el CSS, las imágenes y el JS
app.mount(
    "/static", 
    StaticFiles(directory=base_path / "frontend" / "static"), 
    name="static"
)

# "Montamos" la carpeta templates aunque Nginx o FastAPI normalmente sirven el HTML por rutas
app.mount(
    "/templates", 
    StaticFiles(directory=base_path / "frontend" / "templates"), 
    name="templates"
)

# Registramos todas las rutas que el servidor va a entender
app.include_router(views.route)           # Rutas para ver las páginas HTML
app.include_router(maquina.router)        # Rutas para crear/borrar máquinas
app.include_router(mantenimiento.router)  # Rutas para los mantenimientos
app.include_router(auth.router)           # Rutas de login y seguridad