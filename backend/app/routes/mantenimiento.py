from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.daos.mantenimiento_dao import MantenimientoDAO
from app.daos.maquina_dao import MaquinaDAO
from app.services import ProyectoService

router = APIRouter(prefix="/home/mantenimiento")

# Inyección de dependencias actualizada
dao_mtto = MantenimientoDAO() # MongoDB
dao_maq = MaquinaDAO()        # MySQL
service = ProyectoService(dao_maq, dao_mtto)

class MantenimientoSchema(BaseModel):
    codigo_maquina: str
    empresa: str
    tecnico: str
    tipo: str
    fecha: str
    observaciones: str

@router.post("/agregar")
async def agregar(datos: MantenimientoSchema):
    # El service ahora buscará en MySQL si el codigo_maquina existe
    resultado, error = service.registrar_mantenimiento(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"mensaje": "Mantenimiento guardado exitosamente en MongoDB"}

@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str):
    registros = service.obtener_historial_por_maquina(codigo)
    
    # Convertir ObjectId de MongoDB a String para JSON
    for r in registros:
        if "_id" in r:
            r["_id"] = str(r["_id"])
        
    return registros