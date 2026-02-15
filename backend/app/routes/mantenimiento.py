# ROUTES LIMPIAS - Solo validación HTTP y respuestas
# Responsabilidades: validación de entrada, respuestas HTTP, coordinación con services

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from app.services.mantenimiento_service import MantenimientoService

router = APIRouter(prefix="/api/mantenimiento")
service = MantenimientoService()

# Modelos para validación de entrada
class MantenimientoRequest(BaseModel):
    codigo_maquina: str
    empresa: str
    tecnico: str
    tipo: str
    fecha: str
    observaciones: str
    usuario: str = None

@router.post("/agregar")
async def agregar_mantenimiento(datos: MantenimientoRequest):
    # Registra un nuevo mantenimiento
    try:
        resultado, error = service.registrar_mantenimiento(datos.model_dump())
        if error:
            raise HTTPException(status_code=404 if "no existe" in error else 400, detail=error)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str, response: Response):
    # Obtiene el historial de mantenimientos de una máquina
    # Headers para evitar caché
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    try:
        resultado, error = service.obtener_historial(codigo)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/informe-general")
async def informe_general(codigo: str = None):
    # Genera informe general de mantenimientos
    try:
        resultado, error = service.generar_informe_general(codigo)
        if error:
            raise HTTPException(status_code=500, detail=error)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
