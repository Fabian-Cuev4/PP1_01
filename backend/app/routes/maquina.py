from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services import ProyectoService
from app.repositories import repo_instancia
# Importamos el manager para acceder a Redis
from app.database.database_manager import DatabaseManager

router = APIRouter(prefix="/api/maquinas")
service = ProyectoService(repo_instancia.maquina_dao, repo_instancia.mantenimiento_dao)
redis = DatabaseManager.obtener_redis() # Obtenemos el cliente Redis

# CLAVE DE CACHÉ: Nombre único para guardar la lista de máquinas
CACHE_KEY_LISTA = "maquinas_lista_completa"

class MaquinaSchema(BaseModel):
    codigo_equipo: str
    tipo_equipo: str
    estado_actual: str
    area: str
    fecha: date
    usuario: str = None

@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    nueva, error = service.registrar_maquina(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # INVALIDACIÓN DE CACHÉ: Como agregamos algo nuevo, borramos la caché vieja
    redis.delete(CACHE_KEY_LISTA)
    
    return {"mensaje": "Máquina guardada", "codigo": nueva.codigo_equipo}

@router.put("/actualizar")
async def actualizar_maquina(datos: MaquinaSchema):
    actualizada, error = service.actualizar_maquina(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # INVALIDACIÓN DE CACHÉ: Hubo un cambio, borramos la caché vieja
    redis.delete(CACHE_KEY_LISTA)

    return {"mensaje": "Máquina actualizada", "codigo": actualizada.codigo_equipo}

@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    exito, error = service.eliminar_maquina(codigo)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # INVALIDACIÓN DE CACHÉ: Borramos algo, limpiamos la caché
    redis.delete(CACHE_KEY_LISTA)

    return {"mensaje": "Máquina y mantenimientos eliminados"}

@router.get("/listar")
async def listar_maquinas(response: Response):
    # 1. INTENTO LEER DE REDIS
    datos_en_cache = redis.get(CACHE_KEY_LISTA)
    if datos_en_cache:
        print("⚡ Sirviendo desde Redis (Caché Hit)")
        return datos_en_cache

    # 2. SI NO ESTÁ EN REDIS, VOY A MYSQL
    print("🐢 Consultando MySQL (Caché Miss)")
    try:
        maquinas = repo_instancia.maquina_dao.listar_todas()
        
        # Convertimos los objetos a diccionarios para poder guardarlos en JSON
        # (Asumiendo que listar_todas devuelve objetos, si devuelve dicts, esto varía levemente)
        lista_dicts = [m.__dict__ for m in maquinas] if maquinas else []
        
        # 3. GUARDO EN REDIS POR 10 SEGUNDOS (Polling Interval)
        redis.set(CACHE_KEY_LISTA, lista_dicts, expire=10)
        
        return lista_dicts
    except Exception as e:
        print(f"Error al listar máquinas: {e}")
        return []