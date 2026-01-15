from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from app.repositories import repo_instancia as repo
from app.services import ProyectoService

router = APIRouter()
# Inicializamos el flujo
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
@router.get("/listar/{codigo_maquina}")
async def listar_mantenimientos(codigo_maquina: str):
    #Obtiene todos los mantenimientos de una máquina específica
    mantenimientos, error = service.obtener_historial_mantenimiento(codigo_maquina)
    if error:
        raise HTTPException(status_code=404, detail=error)
    # Convertimos los objetos a una lista de diccionarios para el frontend
    return [
        {
            "empresa": m.empresa,
            "tecnico": m.tecnico,
            "tipo": m.tipo,
            "fecha": str(m.fecha),
            "observaciones": m.observaciones
        } for m in mantenimientos
    ]