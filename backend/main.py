# Este es el archivo principal que inicia el servidor
# Aquí se configura FastAPI y se registran todas las rutas

# Importamos las librerías necesarias
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import os
import logging
from datetime import datetime
import time
from typing import Dict

# Configuramos logging para mostrar mensajes en consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importamos las rutas que hemos creado
from app.routes import maquina, mantenimiento, auth 
# Importamos el gestor de bases de datos
from app.database.database_manager import DatabaseManager

# Esta clase maneja los headers cuando el servidor está detrás de un proxy (como Nginx)
class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    # Este método se ejecuta en cada petición
    async def dispatch(self, request, call_next):
        # EXPLICACIÓN: Obtenemos el ID del servidor desde variables de entorno
        server_id = os.getenv("API_SERVER_ID", "API Desconocido")
        
        # EXPLICACIÓN: Log cada petición recibida con identificación del servidor
        logger.info(f"Petición recibida en {server_id} - {request.method} {request.url.path}")
        
        # Si el proxy envía información sobre el protocolo (http/https), la usamos
        if "x-forwarded-proto" in request.headers:
            request.scope["scheme"] = request.headers["x-forwarded-proto"]
        # Si el proxy envía información sobre el host, la usamos
        if "x-forwarded-host" in request.headers:
            request.scope["server"] = (request.headers["x-forwarded-host"], 
                                       int(request.headers.get("x-forwarded-port", "80")))
        # Si el proxy envía información sobre la IP del cliente, la usamos
        if "x-forwarded-for" in request.headers:
            request.scope["client"] = (request.headers["x-forwarded-for"].split(",")[0], 0)
        # Continuamos con la petición
        response = await call_next(request)
        return response

# Creamos la aplicación FastAPI
app = FastAPI()

# Agregamos los middlewares (componentes que se ejecutan en cada petición)
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Este evento se ejecuta cuando el servidor arranca
@app.on_event("startup")
def startup_db_client():
    # EXPLICACIÓN: Obtenemos el ID del servidor para logs de inicio
    server_id = os.getenv("API_SERVER_ID", "API Desconocido")
    logger.info(f"=== INICIANDO {server_id} ===")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Inicializamos las conexiones a las bases de datos
    DatabaseManager.inicializar()
    
    # EXPLICACIÓN: Log de conexión exitosa a bases de datos
    logger.info(f"Conectado exitosamente al archivador central (MySQL/Mongo)")
    logger.info(f"=== {server_id} LISTO PARA RECIBIR PETICIONES ===")

# Este evento se ejecuta cuando el servidor se apaga
@app.on_event("shutdown")
def shutdown_db_client():
    # EXPLICACIÓN: Obtenemos el ID del servidor para logs de cierre
    server_id = os.getenv("API_SERVER_ID", "API Desconocido")
    logger.info(f"=== CERRANDO {server_id} ===")
    
    # Cerramos las conexiones a las bases de datos
    DatabaseManager.cerrar()
    
    # EXPLICACIÓN: Log de cierre exitoso
    logger.info(f"Conexiones a bases de datos cerradas - {server_id} fuera de línea")

# Registramos todas las rutas (URLs) que el servidor va a manejar

# Endpoint simple para monitoreo (usado por el dashboard)
@app.get("/api/health")
def health_check():
    server_id = os.getenv("API_SERVER_ID", "API Desconocido")
    return {"status": "ok", "server_id": server_id}

_traffic_active_users: Dict[str, float] = {}
_traffic_user_ttl_seconds = 30

@app.post("/api/traffic/ping")
def traffic_ping(username: str = "", is_admin: int = 0):
    if is_admin:
        return {"status": "ignored"}
    if not username or username == "admin":
        return {"status": "ignored"}
    _traffic_active_users[username] = time.time()
    return {"status": "ok"}

@app.get("/api/traffic/stats")
def traffic_stats():
    server_id = os.getenv("API_SERVER_ID", "API Desconocido")
    now = time.time()
    expired = [uname for uname, last_seen in _traffic_active_users.items() if (now - last_seen) > _traffic_user_ttl_seconds]
    for uname in expired:
        _traffic_active_users.pop(uname, None)
    return {
        "status": "ok",
        "server_id": server_id,
        "active_users": len(_traffic_active_users),
    }

app.include_router(maquina.router)        # Rutas para máquinas (/api/maquinas/*)
app.include_router(mantenimiento.router)  # Rutas para mantenimientos (/api/mantenimiento/*)
app.include_router(auth.router)           # Rutas para autenticación (/api/login, /api/register)
