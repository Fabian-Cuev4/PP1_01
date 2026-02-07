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
    server_id = os.getenv("API_SERVER_ID", "Servidor API Desconocido")
    return {"status": "ok", "server_id": server_id}

# Sistema de sesiones persistentes en base de datos (sin TTL)
# Los usuarios permanecen activos hasta que cierran sesión explícitamente

@app.post("/api/traffic/login")
def traffic_login(username: str = "", is_admin: int = 0):
    """Endpoint para registrar cuando un usuario inicia sesión automáticamente"""
    print(f"DEBUG: Login recibido - username='{username}', is_admin={is_admin}")
    
    if is_admin:
        print("DEBUG: Ignorado por ser admin")
        return {"status": "ignored"}
    if not username or username == "admin":
        print(f"DEBUG: Ignorado por username vacío o admin. username='{username}'")
        return {"status": "ignored"}
    
    print(f"DEBUG: Procesando login para usuario '{username}'")
    
    # Registrar en base de datos para persistencia (sin TTL)
    conn = None
    cursor = None
    try:
        from app.database.mysql import MySQLConnection
        conn = MySQLConnection.conectar()
        if not conn:
            return {"status": "error", "message": "No se pudo conectar a la base de datos"}
        
        cursor = conn.cursor()
        server_id = os.getenv("API_SERVER_ID", "Servidor API Desconocido")
        
        # Insertar o actualizar sesión activa
        cursor.execute("""
            INSERT INTO sesiones_activas (username, server_id, is_active) 
            VALUES (%s, %s, TRUE)
            ON DUPLICATE KEY UPDATE 
            is_active = TRUE, 
            last_activity = CURRENT_TIMESTAMP
        """, (username, server_id))
        
        conn.commit()
        
        print(f"DEBUG: Login de '{username}' registrado exitosamente")
        
        return {"status": "ok", "message": f"Usuario {username} ha iniciado sesión (persistente)"}
    except Exception as e:
        print(f"Error registrando login en BD: {e}")
        return {"status": "error", "message": f"Error al registrar login: {str(e)}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.post("/api/traffic/logout")
def traffic_logout(username: str = "", is_admin: int = 0):
    """Endpoint para registrar cuando un usuario cierra sesión automáticamente"""
    if is_admin:
        return {"status": "ignored"}
    if not username or username == "admin":
        return {"status": "ignored"}
    
    # Desactivar en base de datos (sin TTL - persistencia total)
    conn = None
    cursor = None
    try:
        from app.database.mysql import MySQLConnection
        conn = MySQLConnection.conectar()
        if not conn:
            return {"status": "error", "message": "No se pudo conectar a la base de datos"}
        
        cursor = conn.cursor()
        
        # Marcar sesión como inactiva
        cursor.execute("""
            UPDATE sesiones_activas 
            SET is_active = FALSE 
            WHERE username = %s
        """, (username,))
        
        conn.commit()
        
        return {"status": "ok", "message": f"Usuario {username} ha cerrado sesión (persistente)"}
    except Exception as e:
        print(f"Error registrando logout en BD: {e}")
        return {"status": "error", "message": f"Error al registrar logout: {str(e)}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Sistema de sesiones persistentes - SIN TTL
# Los usuarios permanecen activos hasta cierre explícito

@app.get("/api/usuarios/loadbalancer")
def usuarios_loadbalancer():
    """Endpoint para obtener usuarios activos usando el load balancer (sesiones persistentes)"""
    conn = None
    cursor = None
    try:
        # El load balancer distribuye automáticamente entre los servidores disponibles
        # Contamos sesiones activas reales que no han cerrado sesión explícitamente
        from app.database.mysql import MySQLConnection
        conn = MySQLConnection.conectar()
        if not conn:
            return {
                "status": "error",
                "message": "No se pudo conectar a la base de datos",
                "active_users": 0
            }
        
        cursor = conn.cursor(dictionary=True)
        
        # Contar usuarios con sesiones activas (no admin)
        cursor.execute("""
            SELECT COUNT(DISTINCT username) as total 
            FROM sesiones_activas 
            WHERE is_active = TRUE 
            AND username != 'admin'
        """)
        resultado = cursor.fetchone()
        total_usuarios = resultado['total'] if resultado else 0
        
        server_id = os.getenv("API_SERVER_ID", "Servidor API Desconocido")
        return {
            "status": "ok",
            "server_id": server_id,
            "active_users": total_usuarios,
            "source": "sesiones_activas",
            "message": f"Usuarios activos desde {server_id} via load balancer"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al contar usuarios activos: {str(e)}",
            "active_users": 0
        }
    finally:
        # Asegurarse de cerrar siempre cursor y conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.get("/api/usuarios/activos")
def usuarios_activos():
    """Endpoint para contar usuarios reales almacenados en la base de datos"""
    try:
        from app.database.mysql import MySQLConnection
        conn = MySQLConnection.conectar()
        cursor = conn.cursor(dictionary=True)
        
        # Contar todos los usuarios excepto admin
        cursor.execute("SELECT COUNT(*) as total FROM usuarios WHERE username != 'admin'")
        resultado = cursor.fetchone()
        total_usuarios = resultado['total'] if resultado else 0
        
        cursor.close()
        
        server_id = os.getenv("API_SERVER_ID", "Servidor API Desconocido")
        return {
            "status": "ok",
            "server_id": server_id,
            "active_users": total_usuarios,
            "source": "database"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al contar usuarios: {str(e)}",
            "active_users": 0
        }

app.include_router(maquina.router)        # Rutas para máquinas (/api/maquinas/*)
app.include_router(mantenimiento.router)  # Rutas para mantenimientos (/api/mantenimiento/*)
app.include_router(auth.router)           # Rutas para autenticación (/api/login, /api/register)
