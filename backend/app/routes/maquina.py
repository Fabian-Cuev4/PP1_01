# ROUTES LIMPIAS - Solo validación HTTP y respuestas
# Responsabilidades: validación de entrada, respuestas HTTP, coordinación con services

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.maquina_service import MaquinaService
import redis
import os
import json

# Creamos un router para agrupar todas las rutas de máquinas
# El prefix significa que todas las rutas empezarán con /api/maquinas
router = APIRouter(prefix="/api/maquinas")
service = MaquinaService()

# Modelos para validación de entrada
class MaquinaRequest(BaseModel):
    codigo_equipo: str
    tipo_equipo: str
    estado_actual: str
    area: str
    fecha: str
    usuario: str = None

# Creamos la instancia del cliente de Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# Definimos cómo deben ser los datos que recibimos del frontend
# class MaquinaSchema(BaseModel):
#     codigo_equipo: str      # Código único de la máquina
#     tipo_equipo: str         # Tipo: PC o IMP
#     estado_actual: str       # Estado: operativa, fuera de servicio, etc.
#     area: str                # Área donde está ubicada
#     fecha: str               # Fecha de adquisición (acepta string del frontend)
#     usuario: str = None      # Usuario que registró la máquina (opcional)

# Esta ruta se ejecuta cuando el frontend hace POST a /api/maquinas/agregar
@router.post("/agregar")
async def agregar_maquina(datos: MaquinaRequest):
    # Agrega una nueva máquina
    try:

        resultado, error = service.registrar_maquina(datos.model_dump())
        if error:
            raise HTTPException(status_code=400, detail=error)
        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/actualizar")
async def actualizar_maquina(datos: MaquinaRequest):
    # Actualiza una máquina existente
    try:
        # 1. Usamos el service de GitHub para la lógica
        resultado, error = service.actualizar_maquina(datos.model_dump())
        
        if error:
            # Esta lógica de error 404 o 400 es la que trajeron de GitHub, mantenla
            raise HTTPException(status_code=404 if "no existe" in error else 400, detail=error)
        
        # 2. 🔥 TU MEJORA: Actualizamos Redis
        # Borramos la lista general porque un elemento cambió
        redis_client.delete("maquinas:lista")

        # Actualizamos el caché individual (usamos datos.codigo_equipo)
        redis_client.set(
            f"maquina:{datos.codigo_equipo}",
            json.dumps(datos.model_dump()),
            ex=300
        )

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    # Elimina una máquina y sus mantenimientos
    try:
        # 1. Llamamos al servicio (Lógica de GitHub)
        exito, mensaje = service.eliminar_maquina(codigo)
        
        if not exito:
            raise HTTPException(status_code=404, detail=mensaje)
            
        # 2. 🔥 TU MEJORA: Si el servicio borró con éxito, limpiamos Redis
        redis_client.delete("maquinas:lista")
        redis_client.delete(f"maquina:{codigo}")

        return {"mensaje": mensaje}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/listar")
async def listar_maquinas():
    # Lista todas las máquinas usando Caché
    try:
        # 1. Intentamos obtener de Redis (Tu lógica)
        cache = redis_client.get("maquinas:lista")
        if cache:
            return json.loads(cache)

        # 2. Si no hay caché, usamos el Service (Estructura de GitHub)
        maquinas = service.buscar_maquinas()

        # 3. Guardamos en Redis para la próxima consulta (Tu lógica)
        # Nota: El service probablemente ya devuelve strings, 
        # así que el bucle de "fecha" podrías omitirlo si el service ya lo maneja.
        redis_client.set("maquinas:lista", json.dumps(maquinas), ex=300)

        return maquinas

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/buscar")
async def buscar_maquinas(termino: str = None):
    # Esta es la ruta nueva que trajeron de GitHub, la dejamos tal cual
    try:
        maquinas = service.buscar_maquinas(termino)
        return maquinas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
