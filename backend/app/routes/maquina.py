# Este archivo define las rutas (URLs) relacionadas con las máquinas
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend
# CAPA ROUTER: Recibe las peticiones de Polling del Front-end y llama a los Services.

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services.maquina_service import MaquinaService
from app.repositories.proyecto_repository import get_repository

# Creamos un router para agrupar todas las rutas de máquinas
# El prefix significa que todas las rutas empezarán con /api/maquinas
router = APIRouter(prefix="/api/maquinas")

# Obtenemos la instancia del repository y creamos el service
repository = get_repository()
maquina_service = MaquinaService(repository.get_maquina_dao())

# Definimos cómo deben ser los datos que recibimos del frontend
class MaquinaSchema(BaseModel):
    codigo_equipo: str      # Código único de la máquina
    tipo_equipo: str         # Tipo: PC o IMP
    estado_actual: str       # Estado: operativa, fuera de servicio, etc.
    area: str                # Área donde está ubicada
    fecha: str = None       # Fecha de adquisición (opcional, string para evitar validación)
    usuario: str = None      # Usuario que registró la máquina (opcional)

# Esta ruta se ejecuta cuando el frontend hace POST a /api/maquinas/agregar
@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    # Convertimos los datos a un diccionario y los enviamos al servicio
    nueva, error = maquina_service.registrar_maquina(datos.model_dump())
    
    # Si hubo un error (nueva es None), retornamos un error HTTP 400
    if error and nueva is None:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Máquina guardada", "codigo": nueva.codigo_equipo}

# Esta ruta se ejecuta cuando el frontend hace PUT a /api/maquinas/actualizar
@router.put("/actualizar")
async def actualizar_maquina(datos: MaquinaSchema):
    # Enviamos los datos al servicio para actualizar
    actualizada, error = maquina_service.actualizar_maquina(datos.model_dump())
    
    # Si hubo un error (actualizada es None), retornamos un error HTTP 400
    if error and actualizada is None:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Máquina actualizada", "codigo": actualizada.codigo_equipo}

# Esta ruta se ejecuta cuando el frontend hace DELETE a /api/maquinas/eliminar/{codigo}
# El {codigo} es un parámetro que viene en la URL
@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    # Llamamos al servicio para eliminar la máquina
    exito, error = maquina_service.eliminar_maquina(codigo)
    
    # Si hubo un error, retornamos un error HTTP 400
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Máquina y mantenimientos eliminados"}

# Esta ruta se ejecuta cuando el frontend hace GET a /api/maquinas/listar
@router.get("/listar")
async def listar_maquinas(response: Response):
    # Configuramos los headers para que el navegador no guarde una copia en caché
    # Esto asegura que siempre obtengamos los datos más recientes
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    # Pedimos al service que nos traiga todas las máquinas
    maquinas, error = maquina_service.listar_todas_las_maquinas()
    
    # Si hubo un error, lo imprimimos y retornamos una lista vacía
    if error:
        print(f"Error al listar máquinas: {error}")
        return []
    
    # Retornamos la lista de máquinas
    return maquinas

# === RUTAS DE POLLING PARA ACTUALIZACIONES EN TIEMPO REAL ===

# Esta ruta es específica para polling del dashboard
# El frontend la llamará periódicamente para obtener datos actualizados
@router.get("/polling/dashboard")
async def polling_dashboard(response: Response):
    """
    Endpoint de polling para el dashboard principal
    Retorna datos actualizados de máquinas con caché optimizado para polling
    """
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos todas las máquinas (usará caché si está disponible)
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
        
        # Agrupamos por estado
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

# Esta ruta es específica para polling de lista de máquinas
# Útil para tablas que necesitan actualizarse en tiempo real
@router.get("/polling/lista")
async def polling_lista_maquinas(response: Response):
    """
    Endpoint de polling para lista actualizada de máquinas
    Optimizado para actualizaciones frecuentes con caché de corta duración
    """
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos todas las máquinas (usará caché si está disponible)
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

# Esta ruta es para polling de búsqueda de máquinas
@router.get("/polling/buscar/{termino}")
async def polling_buscar_maquinas(termino: str, response: Response):
    """
    Endpoint de polling para búsqueda de máquinas en tiempo real
    """
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Buscamos máquinas por código parcial (usará caché si está disponible)
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

# Esta ruta verifica el estado del sistema de caché
@router.get("/cache/status")
async def cache_status(response: Response):
    """
    Endpoint para verificar el estado del sistema de caché
    Útil para monitoreo y debugging
    """
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
