from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services import ProyectoService
from app.repositories import repo_instancia

# Este archivo crea las rutas o URLs relacionadas con las máquinas
router = APIRouter(prefix="/api/maquinas")

# Usamos el repositorio unificado que ya incluye los DAOs y servicios
service = ProyectoService(repo_instancia.maquina_dao, repo_instancia.mantenimiento_dao)

# Modelo de datos que esperamos recibir cuando se agrega una máquina
class MaquinaSchema(BaseModel):
    codigo_equipo: str
    tipo_equipo: str
    estado_actual: str
    area: str
    fecha: date

# Ruta para guardar una nueva máquina en la base de datos
@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    # Le pedimos al servicio que procese el registro
    nueva, error = service.registrar_maquina(datos.model_dump())
    if error:
        # Si algo falla (ej. código repetido), enviamos el por qué al usuario
        raise HTTPException(status_code=400, detail=error)
    return {"mensaje": "Máquina guardada en MySQL", "codigo": nueva.codigo_equipo}

# Ruta para obtener la lista de todas las máquinas que existen
@router.get("/listar")
async def listar_maquinas(response: Response):
    # Configuramos para que el navegador busque datos frescos y no use copias viejas
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    try:
        maquinas = repo_instancia.maquina_dao.listar_todas()
        return maquinas # Enviamos la lista de máquinas al frontend
    except Exception as e:
        print(f"Error al listar máquinas: {e}")
        return []