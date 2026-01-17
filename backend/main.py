# Este es el archivo principal que arranca todo el servidor (Backend)
# Aquí configuramos FastAPI, las bases de datos y las rutas de la web.

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path
# Importamos las rutas que hemos creado en otros archivos
from app.routes import maquina, mantenimiento, auth 
from app.database.mongodb import MongoDB
from app.database.mysql import MySQLConnection

# Middleware personalizado para manejar headers del proxy
class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Si viene de un proxy, usar los headers X-Forwarded-*
        if "x-forwarded-proto" in request.headers:
            request.scope["scheme"] = request.headers["x-forwarded-proto"]
        if "x-forwarded-host" in request.headers:
            request.scope["server"] = (request.headers["x-forwarded-host"], 
                                       int(request.headers.get("x-forwarded-port", "80")))
        if "x-forwarded-for" in request.headers:
            request.scope["client"] = (request.headers["x-forwarded-for"].split(",")[0], 0)
        response = await call_next(request)
        return response

# Creamos la instancia principal de la aplicación FastAPI
app = FastAPI()

# Agregar middlewares en el orden correcto
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Permitir todas las hosts (por desarrollo)
)

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
    
    #Cerramos las conexiones de forma segura al apagar.
    MongoDB.cerrar()

# Registramos todas las rutas que el servidor va a entender
app.include_router(maquina.router)        # Rutas para crear/borrar máquinas
app.include_router(mantenimiento.router)  # Rutas para los mantenimientos
app.include_router(auth.router)           # Rutas de login y seguridad