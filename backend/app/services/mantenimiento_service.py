# SERVICE - Toda la lógica de negocio de mantenimientos
# Responsabilidades: validación, transformación, normalización, lógica de negocio
# Integrado con Redis Cache e Informe DTO

from app.daos.mantenimiento_dao import MantenimientoDAO
from app.daos.maquina_dao import MaquinaDAO
from app.models.Mantenimiento import Mantenimiento
from app.dtos.informe_dto import InformeMaquinaDTO
from app.database.redis_client import RedisClient
from app.services.maquina_service import MaquinaService
import json

class MantenimientoService:
    def __init__(self):
        self.dao = MantenimientoDAO()
        self.maquina_dao = MaquinaDAO()
        self.maquina_service = MaquinaService()
        # --- Cliente Redis original ---
        self._redis = RedisClient.get_client()
        self._cache_ttl = 120  # segundos

    # Registra nuevo mantenimiento con validación completa
    def registrar_mantenimiento(self, datos: dict) -> tuple:
        # Validación de datos obligatorios
        if not all([datos.get("codigo_maquina"), datos.get("empresa"), 
                   datos.get("tecnico"), datos.get("tipo"), 
                   datos.get("fecha"), datos.get("observaciones")]):
            return None, "Todos los campos son obligatorios"

        codigo_maquina = datos["codigo_maquina"].strip()
        
        # Verificar que la máquina existe (usando el service para aprovechar su lógica)
        maquina = self.maquina_service.obtener_por_codigo(codigo_maquina)
        if not maquina:
            return None, f"La máquina '{codigo_maquina}' no existe"

        # Normalización del tipo de mantenimiento
        tipo = datos["tipo"].strip().lower()
        if tipo not in ["preventivo", "correctivo"]:
            return None, "El tipo debe ser 'preventivo' o 'correctivo'"

        # Creación del objeto mantenimiento
        try:
            mantenimiento = Mantenimiento(
                maquina_objeto=maquina,
                empresa=datos["empresa"].strip(),
                tecnico=datos["tecnico"].strip(),
                tipo=tipo,
                fecha=datos["fecha"].strip(),
                observaciones=datos["observaciones"].strip(),
                usuario=datos.get("usuario", "").strip()
            )

            # Guardado en base de datos
            if self.dao.insertar(
                codigo_maquina,
                datos["empresa"].strip(),
                datos["tecnico"].strip(),
                tipo,
                datos["fecha"].strip(),
                datos["observaciones"].strip(),
                datos.get("usuario", "").strip()
            ):
                # 🔥 INVALIDAR CACHE (Original)
                # Al agregar mantenimiento, el informe de esa máquina y el general cambian
                self._redis.delete(f"informe:{codigo_maquina.lower()}")
                self._redis.delete("informe:all")
                
                return {"mensaje": "Mantenimiento registrado", "codigo_maquina": codigo_maquina}, None
            else:
                return None, "Error al guardar en base de datos"
                
        except ValueError as e:
            return None, str(e)

    # Obtiene historial de mantenimientos de una máquina (ordenado por fecha)
    def obtener_historial(self, codigo_maquina: str) -> tuple:
        codigo_normalizado = codigo_maquina.strip().lower()
        
        # --- Lógica de Caché para Historial (Original) ---
        # Nota: Usamos una clave específica para historial si fuera necesario, 
        # pero aquí priorizamos la consulta fresca o la integración con Informe
        
        # Verificar que la máquina existe
        maquina = self.maquina_service.obtener_por_codigo(codigo_normalizado)
        if not maquina:
            return None, f"La máquina '{codigo_normalizado}' no existe"

        # Obtener mantenimientos ordenados por fecha (más reciente primero)
        mantenimientos = self.dao.listar_por_maquina_ordenados(codigo_normalizado, -1)
        
        # Transformación de datos para el frontend
        resultado = []
        for mant in mantenimientos:
            if "_id" in mant:
                mant["_id"] = str(mant["_id"])
            if "tipo" not in mant:
                mant["tipo"] = "N/A"
            resultado.append(mant)
        
        return resultado, None

    # Genera informe general delegando al DTO con soporte de Redis
    def generar_informe_general(self, codigo_filtro: str = None) -> tuple:
        # --- Lógica de Caché para Informe (Original) ---
        cache_key = f"informe:{codigo_filtro.lower()}" if codigo_filtro else "informe:all"
        
        try:
            cache = self._redis.get(cache_key)
            if cache:
                print(f"⚡ Informe {cache_key} desde Redis")
                return json.loads(cache), None
        except:
            pass

        try:
            # El DTO mismo obtiene y combina los datos de ambas bases
            resultado = InformeMaquinaDTO.crear_reporte_general(codigo_filtro)
            
            # Guardar en caché el resultado (Original)
            try:
                # Si el resultado son objetos DTO, los convertimos a dict
                data_to_cache = [obj.__dict__ if hasattr(obj, '__dict__') else obj for obj in resultado]
                self._redis.setex(
                    cache_key,
                    self._cache_ttl,
                    json.dumps(data_to_cache, default=str)
                )
            except:
                pass

            return resultado, None
        except Exception as e:
            return None, f"Error al generar informe: {str(e)}"

    # Elimina mantenimientos de una máquina
    def eliminar_por_maquina(self, codigo_maquina: str) -> tuple:
        codigo_normalizado = codigo_maquina.strip().lower()
        
        maquina = self.maquina_service.obtener_por_codigo(codigo_normalizado)
        if not maquina:
            return 0, f"La máquina '{codigo_normalizado}' no existe"

        eliminados = self.dao.eliminar_por_maquina(codigo_normalizado)
        
        # 🔥 INVALIDAR CACHE
        self._redis.delete(f"informe:{codigo_normalizado}")
        self._redis.delete("informe:all")
        
        return eliminados, None