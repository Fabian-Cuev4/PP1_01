from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from app.daos.mantenimiento_dao import MantenimientoDAO
from app.daos.maquina_dao import MaquinaDAO
from app.services import ProyectoService

router = APIRouter(prefix="/home/maquinas")

dao_maq = MaquinaDAO()
dao_mtto = MantenimientoDAO()
service = ProyectoService(dao_maq, dao_mtto)

class MaquinaSchema(BaseModel):
    codigo_equipo: str
    tipo_equipo: str
    estado_actual: str
    area: str
    fecha: date

@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    nueva, error = service.registrar_maquina(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"mensaje": "Máquina guardada en MySQL", "codigo": nueva.codigo_equipo}

@router.get("/listar")
async def listar_maquinas():
    return dao_maq.listar_todas()

@router.get("/home/maquinas/informe-general")
async def informe_general():
    return service.obtener_todos_los_informes()