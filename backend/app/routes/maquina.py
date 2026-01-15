from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from app.repositories import repo_instancia
from app.daos.mantenimiento_dao import MantenimientoDAO
from app.services import ProyectoService

router = APIRouter(prefix="/home/maquinas")

# --- AQUÍ ESTÁ LA CORRECCIÓN ---
# Aunque esta ruta sea de máquinas, el Service ahora pide 2 argumentos obligatorios
dao_mtto = MantenimientoDAO() 
service = ProyectoService(repo_instancia, dao_mtto)

class MaquinaSchema(BaseModel):
    codigo_equipo: str
    tipo_equipo: str  # PC o IMP
    estado_actual: str
    area: str
    fecha: date

@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    nueva, error = service.registrar_maquina(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"mensaje": "Máquina agregada a la RAM", "codigo": nueva.codigo_equipo}

@router.get("/listar")
async def listar_maquinas():
    # Accedemos a las máquinas que están en el arreglo de RAM
    maquinas = service._repo.obtener_todas_maquinas()
    return [
        {
            "codigo": m.codigo_equipo,
            "estado": m.estado_actual,
            "area": m.area,
            "tipo": m.tipo_maquina
        } for m in maquinas
    ]