# Este archivo define las rutas (URLs) relacionadas con las máquinas
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.daos.maquina_dao import MaquinaDAO
from app.daos.mantenimiento_dao import MantenimientoDAO
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora

# Creamos un router para agrupar todas las rutas de máquinas
# El prefix significa que todas las rutas empezarán con /api/maquinas
router = APIRouter(prefix="/api/maquinas")

# Creamos instancias directas de los DAOs
maquina_dao = MaquinaDAO()
mantenimiento_dao = MantenimientoDAO()

# Definimos cómo deben ser los datos que recibimos del frontend
class MaquinaSchema(BaseModel):
    codigo_equipo: str      # Código único de la máquina
    tipo_equipo: str         # Tipo: PC o IMP
    estado_actual: str       # Estado: operativa, fuera de servicio, etc.
    area: str                # Área donde está ubicada
    fecha: str               # Fecha de adquisición (acepta string del frontend)
    usuario: str = None      # Usuario que registró la máquina (opcional)

# Esta ruta se ejecuta cuando el frontend hace POST a /api/maquinas/agregar
@router.post("/agregar")
async def agregar_maquina(datos: MaquinaSchema):
    # Convertimos los datos a diccionario
    datos_dict = datos.model_dump()
    
    # Verificamos que no exista otra máquina con el mismo código
    if maquina_dao.buscar_por_codigo(datos_dict.get("codigo_equipo")):
        raise HTTPException(status_code=400, detail=f"El código '{datos_dict.get('codigo_equipo')}' ya existe.")
    
    # Creamos el objeto máquina según el tipo usando Abstract Factory
    tipo = datos_dict.get("tipo_equipo", "").upper()
    try:
        if tipo == "PC":
            nueva = Computadora(
                datos_dict.get("codigo_equipo"), 
                datos_dict.get("estado_actual"), 
                datos_dict.get("area"), 
                datos_dict.get("fecha"),
                datos_dict.get("usuario")
            )
        elif tipo == "IMP":
            nueva = Impresora(
                datos_dict.get("codigo_equipo"), 
                datos_dict.get("estado_actual"), 
                datos_dict.get("area"), 
                datos_dict.get("fecha"),
                datos_dict.get("usuario")
            )
        else:
            raise HTTPException(status_code=400, detail=f"Tipo de equipo '{tipo}' no válido.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Guardamos la máquina
    try:
        maquina_dao.guardar(nueva)
        return {"mensaje": "Máquina guardada", "codigo": nueva.codigo_equipo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar: {str(e)}")

# Esta ruta se ejecuta cuando el frontend hace PUT a /api/maquinas/actualizar
@router.put("/actualizar")
async def actualizar_maquina(datos: MaquinaSchema):
    datos_dict = datos.model_dump()
    codigo = datos_dict.get("codigo_equipo")
    
    if not codigo:
        raise HTTPException(status_code=400, detail="El código de la máquina es obligatorio.")
    
    # Verificamos que la máquina exista
    maquina_db = maquina_dao.buscar_por_codigo(codigo)
    if not maquina_db:
        raise HTTPException(status_code=404, detail=f"La máquina {codigo} no existe.")
    
    # Obtenemos los datos nuevos, si no vienen usamos los antiguos
    tipo = datos_dict.get("tipo_equipo", "").upper() or maquina_db.get('tipo', '').upper()
    estado = datos_dict.get("estado_actual") or maquina_db.get('estado')
    area = datos_dict.get("area") or maquina_db.get('area')
    fecha = datos_dict.get("fecha") or maquina_db.get('fecha')
    usuario = datos_dict.get("usuario") or maquina_db.get('usuario')
    
    # Creamos el objeto máquina según su tipo
    try:
        if tipo in ['COMPUTADORA', 'PC']:
            maquina_obj = Computadora(codigo, estado, area, fecha, usuario)
        elif tipo in ['IMPRESORA', 'IMP']:
            maquina_obj = Impresora(codigo, estado, area, fecha, usuario)
        else:
            raise HTTPException(status_code=400, detail="Tipo de máquina no reconocido.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Actualizamos en la base de datos
    if maquina_dao.actualizar(maquina_obj):
        return {"mensaje": "Máquina actualizada", "codigo": maquina_obj.codigo_equipo}
    else:
        raise HTTPException(status_code=500, detail="Error al actualizar la máquina.")

# Esta ruta se ejecuta cuando el frontend hace DELETE a /api/maquinas/eliminar/{codigo}
@router.delete("/eliminar/{codigo}")
async def eliminar_maquina(codigo: str):
    # Verificamos que la máquina exista
    if not maquina_dao.buscar_por_codigo(codigo):
        raise HTTPException(status_code=404, detail="La máquina no existe.")
    
    # Eliminamos primero todos los mantenimientos de esa máquina
    mantenimiento_dao.eliminar_por_maquina(codigo)
    
    # Luego eliminamos la máquina
    if maquina_dao.eliminar(codigo):
        return {"mensaje": "Máquina y mantenimientos eliminados"}
    else:
        raise HTTPException(status_code=500, detail="Error al eliminar la máquina.")

# Esta ruta se ejecuta cuando el frontend hace GET a /api/maquinas/listar
@router.get("/listar")
async def listar_maquinas():
    try:
        # Pedimos al DAO que nos traiga todas las máquinas
        maquinas = maquina_dao.listar_todas()
        return maquinas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
