# Archivo principal - Configuración FastAPI y registro de rutas

from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import json
import os
from app.routes import maquina, mantenimiento, auth 
from app.database.database_manager import DatabaseManager

# Importar Kafka producer
try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False

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

# Middleware para enviar métricas a Kafka
class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.producer = None
        self.kafka_enabled = False
        if KAFKA_AVAILABLE:
            try:
                kafka_server = os.getenv('KAFKA_SERVER', 'kafka:9092')
                self.producer = KafkaProducer(
                    bootstrap_servers=kafka_server,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    request_timeout_ms=5000,
                    retries=3
                )
                self.kafka_enabled = True
                print(f"✅ Conectado a Kafka en {kafka_server}")
            except Exception as e:
                print(f"⚠️ No se pudo conectar a Kafka: {e}")
                self.kafka_enabled = False
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # Calcular tiempo de respuesta
        process_time = time.time() - start_time
        
        # Obtener ID del servidor
        server_id = os.getenv('SERVER_ID', 'unknown')
        
        # Crear evento de métrica
        event = {
            'server_id': server_id,
            'endpoint': str(request.url.path),
            'method': request.method,
            'status_code': response.status_code,
            'response_time': round(process_time * 1000, 2),  # ms
            'timestamp': time.time(),
            'requests': 1
        }
        
        # Enviar a Kafka si está disponible y no hay error 500
        if self.kafka_enabled and response.status_code < 500:
            try:
                self.producer.send('load-balancer-events', event)
                # No hacer flush para no bloquear
            except Exception as e:
                print(f"⚠️ Error enviando a Kafka: {e}")
                # Deshabilitar Kafka temporalmente para evitar más errores
                self.kafka_enabled = False
        
        return response

# Aplicación FastAPI
app = FastAPI()

# Middlewares
app.add_middleware(MetricsMiddleware)  # Habilitado para enviar métricas al dashboard
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
