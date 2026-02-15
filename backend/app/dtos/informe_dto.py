from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.daos.maquina_dao import MaquinaDAO
from app.daos.mantenimiento_dao import MantenimientoDAO

# DTO para reporte combinado de MySQL (máquinas) y MongoDB (mantenimientos)
# El DTO mismo obtiene los datos de ambas bases de datos
class InformeMaquinaDTO(BaseModel):
    # Datos de MySQL (tabla máquinas)
    codigo: str              # Código del equipo
    tipo: str                # Tipo de equipo (PC/IMP)
    area: str                # Ubicación/área
    estado: str              # Estado actual
    fecha_registro: Optional[str] = None  # Fecha de registro en MySQL
    
    # Datos de MongoDB (colección mantenimientos)
    mantenimientos: List[dict] = []  # Lista de mantenimientos desde MongoDB
    total_mantenimientos: int = 0    # Conteo de mantenimientos
    ultimo_mantenimiento: Optional[str] = None  # Fecha del último mantenimiento
    
    class Config:
        from_attributes = True
    
    @classmethod
    def crear_reporte_general(cls, codigo_filtro: str = None) -> List['InformeMaquinaDTO']:
        # Método estático que obtiene datos de MySQL + MongoDB y crea DTOs
        # El DTO mismo coordina la obtención de datos de ambas bases
        try:
            # DAOs para acceder a ambas bases de datos
            maquina_dao = MaquinaDAO()
            mantenimiento_dao = MantenimientoDAO()
            
            # Obtener máquinas desde MySQL
            if codigo_filtro:
                maquinas = maquina_dao.buscar_similares(codigo_filtro)
            else:
                maquinas = maquina_dao.listar_todas()
            
            if not maquinas:
                return []
            
            # Obtener todos los mantenimientos desde MongoDB con manejo de errores
            try:
                todos_mantenimientos = mantenimiento_dao.listar_todos()
            except Exception as mongo_error:
                # Si MongoDB falla, devolver máquinas sin mantenimientos
                todos_mantenimientos = []
            
            # Agrupar mantenimientos por máquina (case-insensitive)
            mantenimientos_por_maquina = {}
            for mant in todos_mantenimientos:
                codigo_mt = mant.get("codigo_maquina")
                if codigo_mt:
                    codigo_key = str(codigo_mt).strip().lower()
                    if codigo_key not in mantenimientos_por_maquina:
                        mantenimientos_por_maquina[codigo_key] = []
                    
                    # Transformar datos de MongoDB
                    if "_id" in mant:
                        mant["_id"] = str(mant["_id"])
                    if "tipo" not in mant:
                        mant["tipo"] = "N/A"
                    
                    mantenimientos_por_maquina[codigo_key].append(mant)
            
            # Crear DTOs combinando datos de ambas bases
            resultado = []
            for maquina in maquinas:
                codigo_maq = str(maquina.get("codigo", "")).strip().lower()
                mantenimientos = mantenimientos_por_maquina.get(codigo_maq, [])
                
                # Extraer información adicional de mantenimientos
                total_mantenimientos = len(mantenimientos)
                ultimo_mantenimiento = None
                if mantenimientos:
                    # Ordenar por fecha para obtener el más reciente
                    mantenimientos_ordenados = sorted(mantenimientos, 
                                                   key=lambda x: x.get('fecha', ''), 
                                                   reverse=True)
                    ultimo_mantenimiento = mantenimientos_ordenados[0].get('fecha')
                
                # Crear diccionario directamente en lugar de usar DTO
                maquina_dict = {
                    "codigo": maquina["codigo"],
                    "tipo": maquina["tipo"],
                    "area": maquina["area"],
                    "estado": maquina["estado"],
                    "fecha_registro": maquina.get("fecha"),  # Datos de MySQL
                    "mantenimientos": mantenimientos,       # Datos de MongoDB
                    "total_mantenimientos": total_mantenimientos,
                    "ultimo_mantenimiento": ultimo_mantenimiento
                }
                
                resultado.append(maquina_dict)
            
            return resultado
            
        except Exception as e:
            # En caso de cualquier error, devolver una lista vacía en lugar de lanzar excepción
            return []