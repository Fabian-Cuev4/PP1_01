# SERVICE - Toda la lógica de negocio de máquinas
# Integrado con Factory Pattern y Redis Cache

from app.daos.maquina_dao import MaquinaDAO
from app.models.abstrac_factory.MaquinaFactory import MaquinaFactory
from app.database.redis_client import RedisClient
import json

class MaquinaService:
    def __init__(self):
        self.dao = MaquinaDAO()
        # --- Recuperamos tu cliente Redis original ---
        self._redis = RedisClient.get_client()
        self._cache_ttl = 120  # segundos

    def registrar_maquina(self, datos: dict) -> tuple:
        # Validación de datos obligatorios
        if not all([datos.get("codigo_equipo"), datos.get("tipo_equipo"), 
                   datos.get("estado_actual"), datos.get("area"), datos.get("fecha")]):
            return None, "Todos los campos son obligatorios"

        codigo = datos["codigo_equipo"].strip()
        
        # Verificación de duplicados
        if self._existe_codigo(codigo):
            return None, f"El código '{codigo}' ya existe"

        tipo = datos["tipo_equipo"].strip().upper()
        usuario = datos.get("usuario")

        try:
            # --- Reinstalamos el Factory Pattern original ---
            maquina_obj = MaquinaFactory.crear_maquina(
                tipo, 
                codigo, 
                datos.get("estado_actual"), 
                datos.get("area"), 
                datos.get("fecha"),
                usuario
            )

            # Guardado en base de datos
            if self.dao.insertar(
                maquina_obj.codigo_equipo,
                maquina_obj.tipo_equipo,
                maquina_obj.estado_actual,
                maquina_obj.area,
                maquina_obj.fecha,
                maquina_obj.usuario
            ):
                # 🔥 INVALIDAR CACHE (Original)
                self._redis.delete("maquinas:all")
                self._redis.delete(f"maquina:{codigo.lower()}")

                return {"mensaje": "Máquina registrada", "codigo": codigo}, None
            else:
                return None, "Error al guardar en base de datos"
                
        except ValueError as e:
            return None, str(e)

    def actualizar_maquina(self, datos: dict) -> tuple:
        codigo = datos.get("codigo_equipo")
        if not codigo:
            return None, "El código de la máquina es obligatorio"

        maquina_existente = self.dao.buscar_por_codigo_exacto(codigo)
        if not maquina_existente:
            return None, "La máquina no existe"

        # Lógica de mezcla (datos nuevos o antiguos)
        tipo = datos.get("tipo_equipo", "").upper() or maquina_existente.get('tipo', '').upper()
        estado = datos.get("estado_actual") or maquina_existente.get('estado')
        area = datos.get("area") or maquina_existente.get('area')
        fecha = datos.get("fecha") or maquina_existente.get('fecha')
        usuario = datos.get("usuario") or maquina_existente.get('usuario')

        try:
            # --- Usamos la Factory para validar el objeto actualizado ---
            maquina_obj = MaquinaFactory.crear_maquina(tipo, codigo, estado, area, fecha, usuario)
            
            if self.dao.actualizar(
                codigo,
                maquina_obj.tipo_equipo,
                maquina_obj.estado_actual,
                maquina_obj.area,
                maquina_obj.fecha,
                maquina_obj.usuario
            ):
                # 🔥 INVALIDAR CACHE (Original)
                self._redis.delete("maquinas:all")
                self._redis.delete(f"maquina:{codigo.lower()}")
                
                return {"mensaje": "Máquina actualizada", "codigo": codigo}, None
            return None, "Error al actualizar la máquina"
        except ValueError as e:
            return None, str(e)

    def eliminar_maquina(self, codigo: str) -> tuple:
        codigo = codigo.strip()
        if not self.dao.buscar_por_codigo_exacto(codigo):
            return False, "La máquina no existe"

        if self.dao.eliminar(codigo):
            # 🔥 INVALIDAR CACHE (Original)
            self._redis.delete("maquinas:all")
            self._redis.delete(f"maquina:{codigo.lower()}")
            self._redis.delete(f"informe:{codigo.lower()}") # Importante para el DTO
            return True, "Máquina eliminada correctamente"
        return False, "Error al eliminar la máquina"

    def buscar_maquinas(self, termino: str = None) -> list:
        # --- Lógica de Caché para Listado (Original) ---
        if not termino:
            cache_key = "maquinas:all"
            try:
                cache = self._redis.get(cache_key)
                if cache:
                    return json.loads(cache)
            except: pass

        todas = self.dao.listar_todas()
        
        # Convertir objetos date a string para JSON
        for maquina in todas:
            if 'fecha' in maquina and hasattr(maquina['fecha'], 'strftime'):
                maquina['fecha'] = maquina['fecha'].strftime('%Y-%m-%d')
        
        if termino:
            termino_normalizado = termino.strip().lower()
            filtradas = [m for m in todas if termino_normalizado in str(m.get("codigo", "")).lower()]
            return filtradas
        
        # Guardar en caché si es el listado general
        try:
            self._redis.setex("maquinas:all", self._cache_ttl, json.dumps(todas, default=str))
        except: pass
        
        return todas

    def obtener_por_codigo(self, codigo: str) -> dict:
        """Obtiene una máquina por su código"""
        codigo_normalizado = codigo.strip().lower()
        return self.dao.buscar_por_codigo_exacto(codigo_normalizado)

    def _existe_codigo(self, codigo: str) -> bool:
        codigo_normalizado = codigo.strip().lower()
        # Intentamos optimizar buscando en el listado ya cacheado
        todas = self.buscar_maquinas() 
        return any(str(m.get("codigo", "")).lower() == codigo_normalizado for m in todas)