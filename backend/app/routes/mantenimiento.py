from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from app.repositories import repo_instancia # Importamos la instancia de la RAM
from app.daos.mantenimiento_dao import MantenimientoDAO
from app.services import ProyectoService

router = APIRouter(prefix="/home/mantenimiento")

# Inyección de dependencias: Pasamos RAM y Mongo al Service
dao_mtto = MantenimientoDAO()
service = ProyectoService(repo_instancia, dao_mtto)

class MantenimientoSchema(BaseModel):
    codigo_maquina: str
    empresa: str
    tecnico: str
    tipo: str
    fecha: str
    observaciones: str
    

@router.post("/agregar")
async def agregar(datos: MantenimientoSchema):
    resultado, error = service.registrar_mantenimiento(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"mensaje": "Mantenimiento guardado exitosamente en MongoDB"}

@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str):
    """
    Ruta para obtener todo el historial de una sola máquina.
    Trae los datos desde MongoDB.
    """
    registros = service.obtener_historial_por_maquina(codigo)
    
    # IMPORTANTE: Convertir el ObjectId de MongoDB a String para que FastAPI pueda enviarlo
    for r in registros:
        r["_id"] = str(r["_id"])
        
    return registros