# Este archivo define las rutas (URLs) relacionadas con las máquinas
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services import ProyectoService
from app.repositories import repo_instancia

# Creamos un router para agrupar todas las rutas de máquinas
# El prefix significa que todas las rutas empezarán con /api/maquinas
router = APIRouter(prefix="/api/maquinas")

# Creamos una instancia del servicio que maneja la lógica
service = ProyectoService(repo_instancia.maquina_dao, repo_instancia.mantenimiento_dao)

# Definimos cómo deben ser los datos que recibimos del frontend
class MaquinaSchema(BaseModel):
    codigo_equipo: str      # Código único de la máquina
    tipo_equipo: str         # Tipo: PC o IMP
    estado_actual: str       # Estado: operativa, fuera de servicio, etc.
    area: str                # Área donde está ubicada
    fecha: date              # Fecha de adquisición
    usuario: str = None      # Usuario que registró la máquina (opcional)

# Esta ruta se ejecuta cuando el frontend hace POST a /api/maquinas/agregar
@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    # Convertimos los datos a un diccionario y los enviamos al servicio
    nueva, error = service.registrar_maquina(datos.model_dump())
    
    # Si hubo un error, retornamos un error HTTP 400
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Máquina guardada", "codigo": nueva.codigo_equipo}

# Esta ruta se ejecuta cuando el frontend hace PUT a /api/maquinas/actualizar
@router.put("/actualizar")
async def actualizar_maquina(datos: MaquinaSchema):
    # Enviamos los datos al servicio para actualizar
    actualizada, error = service.actualizar_maquina(datos.model_dump())
    
    # Si hubo un error, retornamos un error HTTP 400
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Máquina actualizada", "codigo": actualizada.codigo_equipo}

# Esta ruta se ejecuta cuando el frontend hace DELETE a /api/maquinas/eliminar/{codigo}
# El {codigo} es un parámetro que viene en la URL
@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    # Llamamos al servicio para eliminar la máquina
    exito, error = service.eliminar_maquina(codigo)
    
    # Si hubo un error, retornamos un error HTTP 400
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Máquina y mantenimientos eliminados"}

# Esta ruta se ejecuta cuando el frontend hace GET a /api/maquinas/listar
@router.get("/listar")
async def listar_maquinas(response: Response):
    # Configuramos los headers para que el navegador no guarde una copia en caché
    # Esto asegura que siempre obtengamos los datos más recientes
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    try:
        # Pedimos al DAO que nos traiga todas las máquinas
        maquinas = repo_instancia.maquina_dao.listar_todas()
        # Retornamos la lista de máquinas
        return maquinas
    except Exception as e:
        # Si hay un error, lo imprimimos y retornamos una lista vacía
        print(f"Error al listar máquinas: {e}")
        return []
