# Este archivo define las rutas (URLs) relacionadas con los mantenimientos
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend
# CAPA ROUTER: Recibe las peticiones de Polling del Front-end y llama a los Services.

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services.mantenimiento_service import MantenimientoService
from app.repositories.proyecto_repository import get_repository

# Creamos un router para agrupar todas las rutas de mantenimientos
# El prefix significa que todas las rutas empezarán con /api/mantenimiento
router = APIRouter(prefix="/api/mantenimiento")

# Obtenemos la instancia del repository y creamos el service
repository = get_repository()
mantenimiento_service = MantenimientoService(
    repository.get_mantenimiento_dao(), 
    repository.get_maquina_dao()
)

# Definimos cómo deben ser los datos que recibimos del frontend
class MantenimientoSchema(BaseModel):
    codigo_maquina: str      # Código de la máquina a la que se le hace mantenimiento
    empresa: str              # Nombre de la empresa que hizo el mantenimiento
    tecnico: str              # Nombre del técnico
    tipo: str                 # Tipo: preventivo o correctivo
    fecha: str                # Fecha en que se hizo el mantenimiento
    observaciones: str        # Comentarios sobre el mantenimiento
    usuario: str = None       # Usuario que registró el mantenimiento (opcional)

# Esta ruta se ejecuta cuando el frontend hace POST a /api/mantenimiento/agregar
@router.post("/agregar")
async def agregar(datos: MantenimientoSchema):
    # Convertimos los datos a un diccionario y los enviamos al servicio
    resultado, error = mantenimiento_service.registrar_mantenimiento(datos.model_dump())
    
    # Si hubo un error (resultado es None), retornamos un error HTTP 400
    if error and resultado is None:
        raise HTTPException(status_code=400, detail=error)
    
    # Si todo salió bien, retornamos un mensaje de éxito
    return {"mensaje": "Mantenimiento guardado exitosamente"}

# Esta ruta se ejecuta cuando el frontend hace GET a /api/mantenimiento/listar/{codigo}
# El {codigo} es un parámetro que viene en la URL
@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str, response: Response):
    # Configuramos los headers para que el navegador no guarde una copia en caché
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    # Pedimos al servicio que nos traiga todos los mantenimientos de esa máquina
    registros, error = mantenimiento_service.obtener_historial_por_maquina(codigo)
    
    # Si hubo un error, retornamos un error HTTP 400
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # MongoDB guarda los IDs de forma especial, los convertimos a string
    # para que se puedan enviar como JSON
    for r in registros:
        if "_id" in r:
            r["_id"] = str(r["_id"])
    
    # Retornamos la lista de mantenimientos
    return registros

# Esta ruta se ejecuta cuando el frontend hace GET a /api/mantenimiento/informe-general
# Puede recibir un código opcional como parámetro para filtrar
@router.get("/informe-general")
async def informe_general(codigo: str = None):
    # Pedimos al servicio que genere el reporte completo
    resultado, error = mantenimiento_service.obtener_informe_completo(codigo)
    
    # Si hubo un error, retornamos un error HTTP 404
    if error:
        raise HTTPException(status_code=404, detail=error)
    
    # Si no hay resultados, retornamos un error
    if resultado is None:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
    # Retornamos el reporte
    return resultado

# === RUTAS DE POLLING PARA ACTUALIZACIONES EN TIEMPO REAL ===

# Esta ruta es específica para polling del historial de mantenimientos
@router.get("/polling/historial/{codigo_maquina}")
async def polling_historial_mantenimientos(codigo_maquina: str, response: Response):
    """
    Endpoint de polling para historial de mantenimientos de una máquina específica
    Útil para actualizar en tiempo real el historial cuando se agregan nuevos mantenimientos
    """
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos el historial (usará caché si está disponible)
        registros, error = mantenimiento_service.obtener_historial_por_maquina(codigo_maquina)
        
        if error:
            print(f"Error en polling historial: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        # Convertimos los IDs de MongoDB a string para JSON
        for r in registros:
            if "_id" in r:
                r["_id"] = str(r["_id"])
        
        return {
            "status": "ok",
            "timestamp": str(date.today()),
            "codigo_maquina": codigo_maquina,
            "total": len(registros),
            "datos": registros
        }
        
    except Exception as e:
        print(f"Error general en polling historial: {e}")
        return {"status": "error", "mensaje": str(e), "datos": []}

# Esta ruta es para polling del informe completo de mantenimientos
@router.get("/polling/informe")
async def polling_informe_mantenimientos(response: Response, codigo: str = None):
    """
    Endpoint de polling para informe completo de mantenimientos
    Proporciona datos actualizados para dashboard de mantenimientos
    """
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos el informe completo (usará caché si está disponible)
        resultado, error = mantenimiento_service.obtener_informe_completo(codigo)
        
        if error:
            print(f"Error en polling informe: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        # Preparamos estadísticas adicionales para el dashboard
        total_maquinas = len(resultado)
        total_mantenimientos = sum(len(maquina.get("mantenimientos", [])) for maquina in resultado)
        
        # Agrupamos mantenimientos por tipo
        mantenimientos_por_tipo = {}
        for maquina in resultado:
            for mantenimiento in maquina.get("mantenimientos", []):
                tipo = mantenimiento.get("tipo", "Sin tipo")
                mantenimientos_por_tipo[tipo] = mantenimientos_por_tipo.get(tipo, 0) + 1
        
        return {
            "status": "ok",
            "timestamp": str(date.today()),
            "codigo_filtro": codigo,
            "estadisticas": {
                "total_maquinas": total_maquinas,
                "total_mantenimientos": total_mantenimientos,
                "mantenimientos_por_tipo": mantenimientos_por_tipo
            },
            "datos": resultado
        }
        
    except Exception as e:
        print(f"Error general en polling informe: {e}")
        return {"status": "error", "mensaje": str(e), "datos": []}

# Esta ruta es para polling de todos los mantenimientos del sistema
@router.get("/polling/todos")
async def polling_todos_mantenimientos(response: Response):
    """
    Endpoint de polling para todos los mantenimientos del sistema
    Útil para vistas administrativas que necesitan ver todos los mantenimientos
    """
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos todos los mantenimientos (usará caché si está disponible)
        mantenimientos, error = mantenimiento_service.obtener_todos_los_mantenimientos()
        
        if error:
            print(f"Error en polling todos mantenimientos: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        # Convertimos los IDs de MongoDB a string para JSON
        for m in mantenimientos:
            if "_id" in m:
                m["_id"] = str(m["_id"])
        
        return {
            "status": "ok",
            "timestamp": str(date.today()),
            "total": len(mantenimientos),
            "datos": mantenimientos
        }
        
    except Exception as e:
        print(f"Error general en polling todos mantenimientos: {e}")
        return {"status": "error", "mensaje": str(e), "datos": []}
