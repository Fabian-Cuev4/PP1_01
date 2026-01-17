from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from app.services import ProyectoService
from app.repositories import repo_instancia

# Este archivo crea las rutas relacionadas con los mantenimientos técnicos
router = APIRouter(prefix="/api/mantenimiento")

# Usamos el repositorio unificado que ya incluye los DAOs y servicios
service = ProyectoService(repo_instancia.maquina_dao, repo_instancia.mantenimiento_dao)

# Modelo de los datos que debe enviar el formulario de mantenimiento
class MantenimientoSchema(BaseModel):
    codigo_maquina: str
    empresa: str
    tecnico: str
    tipo: str
    fecha: str
    observaciones: str

# Ruta para guardar un nuevo registro de mantenimiento
@router.post("/agregar")
async def agregar(datos: MantenimientoSchema):
    # Pedimos al servicio que guarde la información en MongoDB
    resultado, error = service.registrar_mantenimiento(datos.model_dump())
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"mensaje": "Mantenimiento guardado exitosamente"}

# Ruta para ver el HISTORIAL de mantenimientos de una máquina específica
@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str, response: Response):
    # Evitamos que el navegador guarde versiones viejas de esta lista
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    # Buscamos en MongoDB todos los registros de ese código
    registros = service.obtener_historial_por_maquina(codigo)
    # Convertimos los IDs extraños de MongoDB a texto normal para el frontend
    for r in registros:
        if "_id" in r:
            r["_id"] = str(r["_id"])
    return registros

# Ruta para el REPORTE GENERAL de todos los mantenimientos (Buscador grande)
@router.get("/informe-general")
async def informe_general(codigo: str = None):
    # Pedimos al servicio que junte datos de MySQL y MongoDB en un solo reporte
    resultado, error = service.obtener_informe_completo(codigo)
    if error:
        raise HTTPException(status_code=404, detail=error)
    if resultado is None:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
    return resultado # Enviamos el reporte completo al frontend