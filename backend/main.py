# Este es el archivo principal que inicia el servidor
# Aquí se configura FastAPI y se registran todas las rutas

# Importamos las librerías necesarias
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
# Importamos las rutas que hemos creado
from app.routes import maquina, mantenimiento, auth 
# Importamos el gestor de bases de datos
from app.database.database_manager import DatabaseManager

# Esta clase maneja los headers cuando el servidor está detrás de un proxy (como Nginx)
class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    # Este método se ejecuta en cada petición
    async def dispatch(self, request, call_next):
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
    # Inicializamos las conexiones a las bases de datos
    DatabaseManager.inicializar()

# Este evento se ejecuta cuando el servidor se apaga
@app.on_event("shutdown")
def shutdown_db_client():
    # Cerramos las conexiones a las bases de datos
    DatabaseManager.cerrar()

# Registramos todas las rutas (URLs) que el servidor va a manejar
app.include_router(maquina.router)        # Rutas para máquinas (/api/maquinas/*)
app.include_router(mantenimiento.router)  # Rutas para mantenimientos (/api/mantenimiento/*)
app.include_router(auth.router)           # Rutas para autenticación (/api/login, /api/register)
