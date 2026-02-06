# Este archivo define las rutas (URLs) relacionadas con las máquinas
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend
# Router solo llama al Service, no conoce la base de datos ni cómo se validan los datos

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services.maquina_service import MaquinaService
from app.repositories.proyecto_repository import get_repository

# Creamos un router para agrupar todas las rutas de máquinas
# El prefix significa que todas las rutas empezarán con /api/maquinas
router = APIRouter(prefix="/api/maquinas")

# Obtenemos la instancia del repository y creamos el service
repository = get_repository()
maquina_service = MaquinaService(repository.get_maquina_dao())

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
    nueva, error = maquina_service.registrar_maquina(datos.model_dump())
    
    # Si hubo un error (nueva es None), retornamos un error HTTP 400
    if error and nueva is None:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Máquina guardada", "codigo": nueva.codigo_equipo}

# Esta ruta se ejecuta cuando el frontend hace PUT a /api/maquinas/actualizar
@router.put("/actualizar")
async def actualizar_maquina(datos: MaquinaSchema):
    # Enviamos los datos al servicio para actualizar
    actualizada, error = maquina_service.actualizar_maquina(datos.model_dump())
    
    # Si hubo un error (actualizada es None), retornamos un error HTTP 400
    if error and actualizada is None:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Máquina actualizada", "codigo": actualizada.codigo_equipo}

# Esta ruta se ejecuta cuando el frontend hace DELETE a /api/maquinas/eliminar/{codigo}
# El {codigo} es un parámetro que viene en la URL
@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    # Llamamos al servicio para eliminar la máquina
    exito, error = maquina_service.eliminar_maquina(codigo)
    
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
    
    # Pedimos al service que nos traiga todas las máquinas
    maquinas, error = maquina_service.listar_todas_las_maquinas()
    
    # Si hubo un error, lo imprimimos y retornamos una lista vacía
    if error:
        print(f"Error al listar máquinas: {error}")
        return []
    
    # Retornamos la lista de máquinas
    return maquinas
