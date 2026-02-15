# Archivo principal - Configuración FastAPI y registro de rutas

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routes import maquina, mantenimiento, auth 
from app.database.database_manager import DatabaseManager

# Middleware para headers de proxy (Nginx)
class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Protocolo desde proxy
        if "x-forwarded-proto" in request.headers:
            request.scope["scheme"] = request.headers["x-forwarded-proto"]
        # Host desde proxy
        if "x-forwarded-host" in request.headers:
            request.scope["server"] = (request.headers["x-forwarded-host"], 
                                       int(request.headers.get("x-forwarded-port", "80")))
        # IP cliente desde proxy
        if "x-forwarded-for" in request.headers:
            request.scope["client"] = (request.headers["x-forwarded-for"].split(",")[0], 0)
        response = await call_next(request)
        return response

# Aplicación FastAPI
app = FastAPI()

# Middlewares
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Evento startup - Inicializar BD
@app.on_event("startup")
def startup_db_client():
    DatabaseManager.inicializar()

# Evento shutdown - Cerrar conexiones
@app.on_event("shutdown")
def shutdown_db_client():
    DatabaseManager.cerrar()

# Registro de rutas
app.include_router(maquina.router)        # /api/maquinas/*
app.include_router(mantenimiento.router)  # /api/mantenimiento/*
app.include_router(auth.router)           # /api/auth/*
