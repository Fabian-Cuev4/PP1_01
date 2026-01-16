from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from app.daos.mantenimiento_dao import MantenimientoDAO
from app.daos.maquina_dao import MaquinaDAO
from app.services import ProyectoService

router = APIRouter(prefix="/home/maquinas")

# Inyección de dependencias actualizada
dao_maq = MaquinaDAO()        # MySQL
dao_mtto = MantenimientoDAO() # MongoDB
service = ProyectoService(dao_maq, dao_mtto)

class MaquinaSchema(BaseModel):
    codigo_equipo: str
    tipo_equipo: str  # PC o IMP
    estado_actual: str
    area: str
    fecha: date

@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    # Esto ahora guarda en la tabla 'maquinas' de MySQL
    nueva, error = service.registrar_maquina(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"mensaje": "Máquina guardada exitosamente en MySQL", "codigo": nueva.codigo_equipo}

@router.get("/listar")
async def listar_maquinas():
    # El service debe tener un método para traer todo de MySQL
    # Si no lo has creado en el service, podemos llamar al DAO directamente aquí
    maquinas = dao_maq.listar_todas() # Asegúrate de tener este método en tu MaquinaDAO
    return maquinas