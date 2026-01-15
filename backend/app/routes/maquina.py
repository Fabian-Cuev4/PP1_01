from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from app.repositories import repo_instancia as repo
from app.services import ProyectoService

router = APIRouter(prefix="/home/maquinas")
service = ProyectoService(repo)

# Agregamos tipo_equipo al modelo de Pydantic
class MaquinaSchema(BaseModel):
    codigo_equipo: str
    estado_actual: str
    area: str
    fecha: date
    tipo_equipo: str

@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    # Ya no instanciamos Maquina aquí. Le pasamos la bola al Service.
    nueva_maquina, error = service.registrar_maquina(datos.model_dump())
    
    if error:
        raise HTTPException(status_code=400, detail=error)
        
    return {"mensaje": f"{nueva_maquina.tipo_maquina} {nueva_maquina.codigo_equipo} guardada"}

@router.get("/listar")
async def listar_maquinas():
    maquinas_objetos = repo.obtener_todas_maquinas()
    return [
        {
            "codigo": m.codigo_equipo, 
            "estado": m.estado_actual,
            "area": m.area,
            "fecha": str(m.fecha),
            "tipo": m.tipo_maquina
        } for m in maquinas_objetos
    ]