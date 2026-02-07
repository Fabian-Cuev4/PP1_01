# Rutas relacionadas con mantenimientos para comunicación frontend-backend
# CAPA ROUTER: Recibe peticiones de Polling y llama a Services

# Importamos librerías necesarias
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from datetime import date
from app.services.mantenimiento_service import MantenimientoService
from app.repositories.proyecto_repository import get_repository

# Router para agrupar rutas de mantenimientos con prefijo /api/mantenimiento
router = APIRouter(prefix="/api/mantenimiento")

# Obtenemos repository y creamos servicio
repository = get_repository()
mantenimiento_service = MantenimientoService(
    repository.get_mantenimiento_dao(), 
    repository.get_maquina_dao()
)

# Schema para datos de mantenimientos recibidos del frontend
class MantenimientoSchema(BaseModel):
    codigo_maquina: str      # Código de la máquina a la que se le hace mantenimiento
    empresa: str              # Nombre de la empresa que hizo el mantenimiento
    tecnico: str              # Nombre del técnico
    tipo: str                 # Tipo: preventivo o correctivo
    fecha: str                # Fecha en que se hizo el mantenimiento
    observaciones: str        # Comentarios sobre el mantenimiento
    usuario: str = None       # Usuario que registró el mantenimiento (opcional)

# Endpoint para agregar nuevo mantenimiento
@router.post("/agregar")
async def agregar(datos: MantenimientoSchema):
    # Convertimos datos a diccionario y enviamos al servicio
    resultado, error = mantenimiento_service.registrar_mantenimiento(datos.model_dump())
    
    # Si hay error, retornamos HTTP 400
    if error and resultado is None:
        raise HTTPException(status_code=400, detail=error)
    
    # Retornamos mensaje de éxito
    return {"mensaje": "Mantenimiento guardado exitosamente"}

# Endpoint para listar mantenimientos de una máquina específica
@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str, response: Response):
    # Configuramos headers para evitar caché
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    # Obtenemos mantenimientos desde el servicio
    registros, error = mantenimiento_service.obtener_historial_por_maquina(codigo)
    
    # Si hay error, retornamos HTTP 400
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Convertimos IDs de MongoDB a string para JSON
    for r in registros:
        if "_id" in r:
            r["_id"] = str(r["_id"])
    
    # Retornamos lista de mantenimientos
    return registros

# Endpoint para informe general de mantenimientos
@router.get("/informe-general")
async def informe_general(codigo: str = None):
    # Generamos reporte completo desde el servicio
    resultado, error = mantenimiento_service.obtener_informe_completo(codigo)
    
    # Si hay error, retornamos HTTP 404
    if error:
        raise HTTPException(status_code=404, detail=error)
    
    # Si no hay resultados, retornamos HTTP 404
    if resultado is None:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
    # Retornamos reporte
    return resultado

# Rutas de polling para actualizaciones en tiempo real

# Endpoint de polling para historial de mantenimientos de máquina específica
@router.get("/polling/historial/{codigo_maquina}")
async def polling_historial_mantenimientos(codigo_maquina: str, response: Response):
    """Endpoint de polling para historial de mantenimientos en tiempo real"""
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos historial (usará caché si disponible)
        registros, error = mantenimiento_service.obtener_historial_por_maquina(codigo_maquina)
        
        if error:
            print(f"Error en polling historial: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        # Convertimos IDs de MongoDB a string para JSON
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

# Endpoint de polling para informe completo de mantenimientos
@router.get("/polling/informe")
async def polling_informe_mantenimientos(response: Response, codigo: str = None):
    """Endpoint de polling para informe completo de mantenimientos"""
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos informe completo (usará caché si disponible)
        resultado, error = mantenimiento_service.obtener_informe_completo(codigo)
        
        if error:
            print(f"Error en polling informe: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        # Preparamos estadísticas adicionales para dashboard
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

# Endpoint de polling para todos los mantenimientos del sistema
@router.get("/polling/todos")
async def polling_todos_mantenimientos(response: Response):
    """Endpoint de polling para todos los mantenimientos del sistema"""
    # Configuramos headers para polling
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    try:
        # Obtenemos todos los mantenimientos (usará caché si disponible)
        mantenimientos, error = mantenimiento_service.obtener_todos_los_mantenimientos()
        
        if error:
            print(f"Error en polling todos mantenimientos: {error}")
            return {"status": "error", "mensaje": error, "datos": []}
        
        # Convertimos IDs de MongoDB a string para JSON
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
