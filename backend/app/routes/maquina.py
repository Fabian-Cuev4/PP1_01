from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services import ProyectoService
from app.repositories import repo_instancia
# IMPORTAMOS EL MANAGER PARA USAR REDIS
from app.database.database_manager import DatabaseManager
import json

router = APIRouter(prefix="/api/maquinas")
service = ProyectoService(repo_instancia.maquina_dao, repo_instancia.mantenimiento_dao)

# CLAVE PARA GUARDAR EN REDIS
KEY_CACHE_MAQUINAS = "cache_lista_maquinas"

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
    
    # SI CAMBIAN LOS DATOS, BORRAMOS LA CACHÉ VIEJA
    redis = DatabaseManager.obtener_redis()
    redis.delete(KEY_CACHE_MAQUINAS)
    
    return {"mensaje": "Máquina guardada", "codigo": nueva.codigo_equipo}

@router.put("/actualizar")
async def actualizar_maquina(datos: MaquinaSchema):
    actualizada, error = service.actualizar_maquina(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # SI CAMBIAN LOS DATOS, BORRAMOS LA CACHÉ VIEJA
    redis = DatabaseManager.obtener_redis()
    redis.delete(KEY_CACHE_MAQUINAS)

    return {"mensaje": "Máquina actualizada", "codigo": actualizada.codigo_equipo}

@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    exito, error = service.eliminar_maquina(codigo)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # SI CAMBIAN LOS DATOS, BORRAMOS LA CACHÉ VIEJA
    redis = DatabaseManager.obtener_redis()
    redis.delete(KEY_CACHE_MAQUINAS)

    return {"mensaje": "Máquina y mantenimientos eliminados"}

@router.get("/listar")
async def listar_maquinas(response: Response):
    # EVITAR QUE EL NAVEGADOR GUARDE CACHÉ (Queremos que el polling funcione real)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    redis = DatabaseManager.obtener_redis()
    
    # 1. INTENTAR LEER DE REDIS
    datos_cache = redis.get(KEY_CACHE_MAQUINAS)
    if datos_cache:
        print("⚡ CACHÉ HIT: Sirviendo desde Redis")
        return datos_cache

    # 2. SI NO HAY CACHÉ, LEER DE MYSQL
    print("🐢 CACHÉ MISS: Consultando base de datos...")
    try:
        maquinas = repo_instancia.maquina_dao.listar_todas()
        
        # Convertimos objetos a diccionarios para poder enviarlos
        # Ajuste rápido: asumiendo que maquinas es una lista de objetos
        lista_final = [m.__dict__ for m in maquinas] if maquinas else []
        
        # 3. GUARDAR EN REDIS (EXPIRA EN 10 SEGUNDOS)
        redis.set(KEY_CACHE_MAQUINAS, lista_final, expire=10)
        
        return lista_final
    except Exception as e:
        print(f"Error: {e}")
        return []