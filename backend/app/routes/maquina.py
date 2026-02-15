# ROUTES LIMPIAS - Solo validación HTTP y respuestas
# Responsabilidades: validación de entrada, respuestas HTTP, coordinación con services

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.maquina_service import MaquinaService

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
        resultado, error = service.actualizar_maquina(datos.model_dump())
        if error:
            raise HTTPException(status_code=404 if "no existe" in error else 400, detail=error)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    # Elimina una máquina y sus mantenimientos
    try:
        exito, mensaje = service.eliminar_maquina(codigo)
        if not exito:
            raise HTTPException(status_code=404, detail=mensaje)
        return {"mensaje": mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/listar")
async def listar_maquinas():
    # Lista todas las máquinas
    try:
        maquinas = service.buscar_maquinas()
        return maquinas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/buscar")
async def buscar_maquinas(termino: str = None):
    # Busca máquinas por término parcial
    try:
        maquinas = service.buscar_maquinas(termino)
        return maquinas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
