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

@router.get("/verificar-codigo/{codigo}")
async def verificar_codigo(codigo: str):
    """Verifica si un código de máquina ya existe"""
    maquina = dao_maq.buscar_por_codigo(codigo)
    return {"existe": maquina is not None, "codigo": codigo}