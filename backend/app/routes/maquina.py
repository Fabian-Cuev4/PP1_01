from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from app.models.Maquina import Maquina  # Importas el modelo con getters/setters
from app.repositories import repo_instancia as repo

router = APIRouter(prefix="/home/maquinas")


# Modelo de datos (Pydantic)
class MaquinaSchema(BaseModel):
    codigo_equipo: str
    estado_actual: str
    area: str
    fecha: date

#Rutas funcionales
@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    nueva_maquina = Maquina(datos.codigo_equipo, datos.estado_actual, datos.area, datos.fecha)
    repo.guardar_maquina(nueva_maquina)
    return {"mensaje": f"Máquina {nueva_maquina.codigo_equipo} guardada"}
@router.get("/listar")
async def listar_maquinas():
    maquinas_objetos = repo.obtener_todas_maquinas()
    # Conversion a JSON
    return [
        {
            "codigo": m.codigo_equipo, 
            "estado": m.estado_actual, 
            "area": m.area,
            "fecha": str(m.fecha)
        } for m in maquinas_objetos
    ]
