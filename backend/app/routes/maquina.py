# Rutas relacionadas con máquinas para comunicación frontend-backend
# CAPA ROUTER: Recibe peticiones de Polling y llama a Services

# Importamos librerías necesarias
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services.maquina_service import MaquinaService
from app.repositories.proyecto_repository import get_repository

# Router para agrupar rutas de máquinas con prefijo /api/maquinas
router = APIRouter(prefix="/api/maquinas")

# Obtenemos repository y creamos servicio
repository = get_repository()
maquina_service = MaquinaService(repository.get_maquina_dao())

# Schema para datos de máquinas recibidos del frontend
class MaquinaSchema(BaseModel):
    codigo_equipo: str      # Código único de la máquina
    tipo_equipo: str         # Tipo: PC o IMP
    estado_actual: str       # Estado: operativa, fuera de servicio, etc.
    area: str                # Área donde está ubicada
    fecha: str = None       # Fecha de adquisición (opcional)
    usuario: str = None      # Usuario que registró la máquina (opcional)

# Endpoint para agregar nueva máquina
@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    # Convertimos datos a diccionario y enviamos al servicio
    nueva, error = maquina_service.registrar_maquina(datos.model_dump())
    
    # Si hay error, retornamos HTTP 400
    if error and nueva is None:
        raise HTTPException(status_code=400, detail=error)
    
    # Retornamos mensaje de éxito
    return {"mensaje": "Máquina guardada", "codigo": nueva.codigo_equipo}

# Endpoint para actualizar máquina existente
@router.put("/actualizar")
async def actualizar_maquina(datos: MaquinaSchema):
    # Enviamos datos al servicio para actualizar
    actualizada, error = maquina_service.actualizar_maquina(datos.model_dump())
    
    # Si hay error, retornamos HTTP 400
    if error and actualizada is None:
        raise HTTPException(status_code=400, detail=error)
    
    # Retornamos mensaje de éxito
    return {"mensaje": "Máquina actualizada", "codigo": actualizada.codigo_equipo}

# Endpoint para eliminar máquina por código
@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    # Llamamos al servicio para eliminar la máquina
    exito, error = maquina_service.eliminar_maquina(codigo)
    
    # Si hay error, retornamos HTTP 400
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Retornamos mensaje de éxito
    return {"mensaje": "Máquina y mantenimientos eliminados"}

# Endpoint para listar todas las máquinas
@router.get("/listar")
async def listar_maquinas(response: Response):
    # Configuramos headers para evitar caché
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    # Obtenemos todas las máquinas desde el servicio
    maquinas, error = maquina_service.listar_todas_las_maquinas()
    
    # Si hay error, imprimimos y retornamos lista vacía
    if error:
        print(f"Error al listar máquinas: {error}")
        return []
    
    # Retornamos lista de máquinas
    return maquinas

# Rutas de polling para actualizaciones en tiempo real

# Endpoint de polling para dashboard principal
@router.get("/polling/dashboard")
async def polling_dashboard(response: Response):
    """Endpoint de polling para dashboard con datos actualizados de máquinas"""
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos todas las máquinas (usará caché si disponible)
        maquinas, error = maquina_service.listar_todas_las_maquinas()
        
        if error:
            print(f"Error en polling dashboard: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        # Preparamos datos específicos para dashboard
        dashboard_data = {
            "status": "ok",
            "timestamp": str(date.today()),
            "total_maquinas": len(maquinas),
            "maquinas_por_estado": {},
            "maquinas_por_tipo": {},
            "maquinas_por_area": {},
            "datos_completos": maquinas
        }
        
        # Agrupamos máquinas por estado, tipo y área
        for maquina in maquinas:
            estado = maquina.get("estado", "Sin estado")
            dashboard_data["maquinas_por_estado"][estado] = dashboard_data["maquinas_por_estado"].get(estado, 0) + 1
            
            tipo = maquina.get("tipo", "Sin tipo")
            dashboard_data["maquinas_por_tipo"][tipo] = dashboard_data["maquinas_por_tipo"].get(tipo, 0) + 1
            
            area = maquina.get("area", "Sin área")
            dashboard_data["maquinas_por_area"][area] = dashboard_data["maquinas_por_area"].get(area, 0) + 1
        
        return dashboard_data
        
    except Exception as e:
        print(f"Error general en polling dashboard: {e}")
        return {"status": "error", "mensaje": str(e), "datos": []}

# Endpoint de polling para lista actualizada de máquinas
@router.get("/polling/lista")
async def polling_lista_maquinas(response: Response):
    """Endpoint de polling para lista de máquinas con actualizaciones frecuentes"""
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos todas las máquinas (usará caché si disponible)
        maquinas, error = maquina_service.listar_todas_las_maquinas()
        
        if error:
            print(f"Error en polling lista: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        return {
            "status": "ok",
            "timestamp": str(date.today()),
            "total": len(maquinas),
            "datos": maquinas
        }
        
    except Exception as e:
        print(f"Error general en polling lista: {e}")
        return {"status": "error", "mensaje": str(e), "datos": []}

# Endpoint de polling para búsqueda de máquinas en tiempo real
@router.get("/polling/buscar/{termino}")
async def polling_buscar_maquinas(termino: str, response: Response):
    """Endpoint de polling para búsqueda de máquinas por código parcial"""
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Buscamos máquinas por código parcial (usará caché si disponible)
        maquinas, error = maquina_service.buscar_maquinas_por_codigo(termino)
        
        if error:
            print(f"Error en polling búsqueda: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        return {
            "status": "ok",
            "timestamp": str(date.today()),
            "termino": termino,
            "total": len(maquinas),
            "datos": maquinas
        }
        
    except Exception as e:
        print(f"Error general en polling búsqueda: {e}")
        return {"status": "error", "mensaje": str(e), "datos": []}

# Endpoint para verificar estado del sistema de caché
@router.get("/cache/status")
async def cache_status(response: Response):
    """Endpoint para verificar estado del sistema de caché (monitoreo)"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    try:
        from app.database.redis import RedisConnection
        
        redis_disponible = RedisConnection.esta_disponible()
        
        return {
            "status": "ok",
            "redis_disponible": redis_disponible,
            "mensaje": "Redis disponible" if redis_disponible else "Redis no disponible - funcionando sin caché"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "redis_disponible": False,
            "mensaje": f"Error al verificar caché: {str(e)}"
        }
