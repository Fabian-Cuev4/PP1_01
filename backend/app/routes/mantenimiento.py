from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from app.repositories import ProyectoRepository
from app.services import ProyectoService

router = APIRouter()

# Inicializamos el flujo
repo = ProyectoRepository()
service = ProyectoService(repo)

class MantenimientoSchema(BaseModel):
    codigo_maquina: str # Necesario para buscar la máquina
    empresa: str
    tecnico: str
    tipo: str
    fecha: date
    observaciones: str

@router.post("/agregar")
async def agregar_mantenimiento(datos: MantenimientoSchema):
    # Convertimos el esquema Pydantic a diccionario para el service
    resultado, error = service.registrar_mantenimiento(datos.model_dump())

    if error:
        raise HTTPException(status_code=404, detail=error)
    
    return {
        "mensaje": "Mantenimiento registrado con éxito",
        "codigo_confirmado": resultado.codigo_maquina_vinculada
    }