# Este archivo define las rutas (URLs) relacionadas con los mantenimientos
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from app.daos.maquina_dao import MaquinaDAO
from app.daos.mantenimiento_dao import MantenimientoDAO
from app.models.Mantenimiento import Mantenimiento
from app.dtos.informe_dto import InformeMaquinaDTO

# Creamos un router para agrupar todas las rutas de mantenimientos
# El prefix significa que todas las rutas empezarán con /api/mantenimiento
router = APIRouter(prefix="/api/mantenimiento")

# Creamos instancias directas de los DAOs
maquina_dao = MaquinaDAO()
mantenimiento_dao = MantenimientoDAO()

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
    datos_dict = datos.model_dump()
    codigo = datos_dict.get("codigo_maquina")
    
    # Verificamos que la máquina exista
    maquina_db = maquina_dao.buscar_por_codigo(codigo)
    if not maquina_db:
        raise HTTPException(status_code=404, detail=f"La máquina {codigo} no existe.")
    
    # Creamos el objeto mantenimiento
    nuevo_mtto = Mantenimiento(
        maquina_db,  # Pasamos el objeto máquina encontrado
        datos_dict.get("empresa"),
        datos_dict.get("tecnico"),
        datos_dict.get("tipo"),
        datos_dict.get("fecha"),
        datos_dict.get("observaciones"),
        datos_dict.get("usuario")
    )
    
    # Guardamos el mantenimiento
    mantenimiento_dao.guardar(nuevo_mtto)
    return {"mensaje": "Mantenimiento registrado", "codigo_maquina": codigo}

# Esta ruta se ejecuta cuando el frontend hace GET a /api/mantenimiento/listar/{codigo}
@router.get("/listar/{codigo}")
async def listar_mantenimientos_equipo(codigo: str, response: Response):
    # Configuramos los headers para que el navegador no guarde una copia en caché
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    # Pedimos al DAO que nos traiga todos los mantenimientos de esa máquina
    registros = mantenimiento_dao.listar_por_maquina(codigo)
    
    # MongoDB guarda los IDs de forma especial, los convertimos a string
    for r in registros:
        if "_id" in r:
            r["_id"] = str(r["_id"])
    
    return registros

# Esta ruta se ejecuta cuando el frontend hace GET a /api/mantenimiento/informe-general
@router.get("/informe-general")
async def informe_general(codigo: str = None):
    try:
        # Obtenemos todas las máquinas
        todas_las_maquinas = maquina_dao.listar_todas()
        
        # Si nos dieron un código, filtramos solo esa máquina
        if codigo:
            todas_las_maquinas = [m for m in todas_las_maquinas if m.get("codigo") == codigo]
        
        if not todas_las_maquinas:
            return []
        
        # Obtenemos todos los mantenimientos
        todos_mttos = mantenimiento_dao.listar_todos() or []
        
        # Agrupamos los mantenimientos por código de máquina
        mttos_por_maquina = {}
        for mt in todos_mttos:
            codigo_mt = mt.get("codigo_maquina")
            if codigo_mt:
                codigo_key = str(codigo_mt).strip().lower()
                if codigo_key not in mttos_por_maquina:
                    mttos_por_maquina[codigo_key] = []
                if "_id" in mt:
                    mt["_id"] = str(mt["_id"])
                if "tipo" not in mt:
                    mt["tipo"] = "N/A"
                mttos_por_maquina[codigo_key].append(mt)
        
        # Construimos el reporte final usando DTO
        resultado = []
        for maq in todas_las_maquinas:
            codigo_maq = str(maq.get("codigo", "")).strip().lower()
            mttos = mttos_por_maquina.get(codigo_maq, [])
            
            resultado.append({
                "codigo": maq["codigo"],
                "tipo": maq["tipo"],
                "area": maq["area"],
                "estado": maq["estado"],
                "mantenimientos": mttos  # Aseguramos que sea una lista
            })
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar informe: {str(e)}")
