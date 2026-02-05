# Este archivo define las rutas (URLs) relacionadas con los mantenimientos
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, Response, Request, Query
from pydantic import BaseModel
from app.services import ProyectoService
from app.repositories import repo_instancia
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Creamos un router para agrupar todas las rutas de mantenimientos
# El prefix significa que todas las rutas empezarán con /api/mantenimiento
router = APIRouter(prefix="/api/mantenimiento")

# Creamos una instancia del servicio que maneja la lógica
service = ProyectoService(repo_instancia.maquina_dao, repo_instancia.mantenimiento_dao)

# Definimos cómo deben ser los datos que recibimos del frontend
class MantenimientoSchema(BaseModel):
    codigo_maquina: str      # Código de la máquina a la que se le hace mantenimiento
    empresa: str              # Nombre de la empresa que hizo el mantenimiento
    tecnico: str              # Nombre del técnico
    tipo: str                 # Tipo: preventivo o correctivo
    fecha: str                # Fecha en que se hizo el mantenimiento
    observaciones: str        # Comentarios sobre el mantenimiento
    usuario: str = None       # Usuario que registró el mantenimiento (opcional)

# Esta ruta se ejecuta cuando el frontend hace POST a /api/mantenimiento/agregar
@router.post("/agregar")
async def agregar(datos: MantenimientoSchema, request: Request):
    # Obtener IP del cliente
    client_ip = request.client.host
    client_port = request.client.port
    
    # Convertimos los datos a un diccionario y los enviamos al servicio
    resultado, error = service.registrar_mantenimiento(datos.model_dump())
    
    # Log de la petición
    logger.info(f"{client_ip}:{client_port} - \"POST /api/mantenimiento/agregar HTTP/1.0\" 200 OK")
    
    # Si hubo un error, retornamos un error HTTP 400
    if error:
        logger.info(f"{client_ip}:{client_port} - \"POST /api/mantenimiento/agregar HTTP/1.0\" 400 Bad Request")
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Mantenimiento guardado exitosamente"}

# Esta ruta se ejecuta cuando el frontend hace GET a /api/mantenimiento/listar/{codigo}
# El {codigo} es un parámetro que viene en la URL
@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str, response: Response, request: Request):
    # Obtener IP del cliente
    client_ip = request.client.host
    client_port = request.client.port
    
    # Configuramos los headers para que el navegador no guarde una copia en caché
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    # Pedimos al servicio que nos traiga todos los mantenimientos de esa máquina
    registros = service.obtener_historial_por_maquina(codigo)
    
    # Log de la petición
    logger.info(f"{client_ip}:{client_port} - \"GET /api/mantenimiento/listar/{codigo} HTTP/1.0\" 200 OK")
    
    # MongoDB guarda los IDs de forma especial, los convertimos a string
    # para que se puedan enviar como JSON
    for r in registros:
        if "_id" in r:
            r["_id"] = str(r["_id"])
    
    # Retornamos la lista de mantenimientos
    return registros

# Esta ruta se ejecuta cuando el frontend hace GET a /api/mantenimiento/informe-general
# Puede recibir un código opcional como parámetro para filtrar
@router.get("/informe-general")
async def informe_general(request: Request, codigo: str = Query(None)):
    # Obtener IP del cliente
    client_ip = request.client.host
    client_port = request.client.port
    
    # Pedimos al servicio que genere el reporte completo
    resultado, error = service.obtener_informe_completo(codigo)
    
    # Log de la petición
    logger.info(f"{client_ip}:{client_port} - \"GET /api/mantenimiento/informe-general HTTP/1.0\" 200 OK")
    
    # Si hubo un error, retornamos un error HTTP 404
    if error:
        logger.info(f"{client_ip}:{client_port} - \"GET /api/mantenimiento/informe-general HTTP/1.0\" 404 Not Found")
        raise HTTPException(status_code=404, detail=error)
    
    # Si no hay resultados, retornamos un error
    if resultado is None:
        logger.info(f"{client_ip}:{client_port} - \"GET /api/mantenimiento/informe-general HTTP/1.0\" 404 Not Found")
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
    # Retornamos el reporte
    return resultado
