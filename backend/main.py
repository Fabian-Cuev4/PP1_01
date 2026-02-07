# Este es el archivo principal que inicia el servidor
# Aquí se configura FastAPI y se registran todas las rutas

# Importamos librerías necesarias para FastAPI y middleware
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import os
import logging
from datetime import datetime

# Configuramos logging básico para mostrar mensajes en consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importamos rutas de la aplicación
from app.routes import maquina, mantenimiento, auth
# Importamos gestor de bases de datos
from app.database.database_manager import DatabaseManager

# Middleware para manejar headers cuando está detrás de proxy (Nginx)
class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    # Método que se ejecuta en cada petición entrante
    async def dispatch(self, request, call_next):
        # Obtenemos ID del servidor desde variables de entorno
        server_id = os.getenv("API_SERVER_ID", "API Desconocido")
        
        # Registramos cada petición con identificación del servidor
        logger.info(f"Petición recibida en {server_id} - {request.method} {request.url.path}")
        
        # Procesamos headers de proxy si existen
        if "x-forwarded-proto" in request.headers:
            request.scope["scheme"] = request.headers["x-forwarded-proto"]
        if "x-forwarded-host" in request.headers:
            request.scope["server"] = (request.headers["x-forwarded-host"], 
                                       int(request.headers.get("x-forwarded-port", "80")))
        if "x-forwarded-for" in request.headers:
            request.scope["client"] = (request.headers["x-forwarded-for"].split(",")[0], 0)
        
        # Continuamos con el procesamiento de la petición
        response = await call_next(request)
        return response

# Creamos aplicación FastAPI
app = FastAPI()

# Agregamos middlewares para proxy y hosts confiables
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Evento que se ejecuta al iniciar el servidor
@app.on_event("startup")
def startup_db_client():
    # Obtenemos ID del servidor para logs
    server_id = os.getenv("API_SERVER_ID", "API Desconocido")
    logger.info(f"=== INICIANDO {server_id} ===")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Inicializamos conexiones a bases de datos
    DatabaseManager.inicializar()
    
    # Registramos conexión exitosa
    logger.info(f"Conectado exitosamente al archivador central (MySQL/Mongo)")
    logger.info(f"=== {server_id} LISTO PARA RECIBIR PETICIONES ===")

# Evento que se ejecuta al apagar el servidor
@app.on_event("shutdown")
def shutdown_db_client():
    # Obtenemos ID del servidor para logs
    server_id = os.getenv("API_SERVER_ID", "API Desconocido")
    logger.info(f"=== CERRANDO {server_id} ===")
    
    # Cerramos conexiones a bases de datos
    DatabaseManager.cerrar()
    
    # Registramos cierre exitoso
    logger.info(f"Conexiones a bases de datos cerradas - {server_id} fuera de línea")

# Registramos todas las rutas (URLs) que el servidor va a manejar

# Endpoint simple para monitoreo del sistema
@app.get("/api/health")
def health_check():
    server_id = os.getenv("API_SERVER_ID", "Servidor API Desconocido")
    return {"status": "ok", "server_id": server_id}

# Registramos rutas principales de la aplicación
app.include_router(maquina.router)        # Rutas para máquinas (/api/maquinas/*)
app.include_router(mantenimiento.router)  # Rutas para mantenimientos (/api/mantenimiento/*)
app.include_router(auth.router)           # Rutas para autenticación (/api/login, /api/register)
