from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.daos.mantenimiento_dao import MantenimientoDAO
from app.daos.maquina_dao import MaquinaDAO
from app.services import ProyectoService

router = APIRouter(prefix="/home/mantenimiento")

dao_mtto = MantenimientoDAO()
dao_maq = MaquinaDAO()
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
    resultado, error = service.registrar_mantenimiento(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"mensaje": "Mantenimiento guardado exitosamente"}

# HISTORIAL INDIVIDUAL
@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str):
    registros = service.obtener_historial_por_maquina(codigo)
    for r in registros:
        if "_id" in r:
            r["_id"] = str(r["_id"])
    return registros

# REPORTE GENERAL (BUSCADOR VENTANA 3)
@router.get("/informe-general")
async def informe_general(codigo: str = None):
    resultado, error = service.obtener_informe_completo(codigo)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return resultado