# Lógica de negocio de máquinas
# Service es el cerebro: valida y coordina operaciones
# CAPA SERVICE: Antes de ir al DAO, pide cliente Redis al DatabaseManager
# Si hay "Cache Hit", devuelve datos al Front
# Escritura e Invalidación: Llama a DatabaseManager.limpiar_cache_sistema()

# Importamos clases necesarias
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora
from app.database.database_manager import DatabaseManager
from app.database.redis import RedisConnection

class MaquinaService:
    # Coordina todas las operaciones de máquinas (PC e IMP)
    # Es el CEREBRO que maneja caché y coordina con el DAO
    
    def __init__(self, maquina_dao):
        # Guardamos referencia al DAO para uso posterior
        self._maquina_dao = maquina_dao
    
    def registrar_maquina(self, datos_dict):
        # Registra nueva máquina en el sistema
        # ESCRITURA: Invalidamos caché después de guardar
        
        # Validación: código es obligatorio
        codigo = datos_dict.get("codigo_equipo")
        if not codigo or codigo.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Validación: código debe ser único
        maquina_existente = self._maquina_dao.buscar_por_codigo(codigo)
        if maquina_existente:
            return None, f"El código '{codigo}' ya existe"
        
        # Validación: tipo es obligatorio y debe ser PC o IMP
        tipo = datos_dict.get("tipo_equipo", "").upper()
        if not tipo:
            return None, "El tipo de equipo es obligatorio"
        
        if tipo not in ["PC", "IMP"]:
            return None, "El tipo de equipo debe ser exactamente PC o IMP"
        
        # Validación: otros campos obligatorios
        if not datos_dict.get("estado_actual"):
            return None, "El estado actual es obligatorio"
        
        if not datos_dict.get("area"):
            return None, "El área es obligatoria"
        
        # Manejo de fecha opcional
        fecha_str = datos_dict.get("fecha", "").strip()
        fecha_obj = None
        
        if fecha_str:
            try:
                from datetime import datetime
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                return None, f"Formato de fecha inválido: {fecha_str}. Use YYYY-MM-DD"
        
        # Manejo de usuario opcional
        usuario_str = datos_dict.get("usuario", "").strip()
        if not usuario_str:
            usuario_str = None
        
        # Creamos objeto máquina según su tipo
        try:
            if tipo == "PC":
                nueva_maquina = Computadora(
                    codigo,
                    datos_dict.get("estado_actual"),
                    datos_dict.get("area"),
                    fecha_obj,
                    usuario_str
                )
            elif tipo == "IMP":
                nueva_maquina = Impresora(
                    codigo,
                    datos_dict.get("estado_actual"),
                    datos_dict.get("area"),
                    fecha_obj,
                    usuario_str
                )
            
            # Guardamos máquina en base de datos
            resultado = self._maquina_dao.guardar(nueva_maquina)
            
            if resultado:
                # ESCRITURA: Invalidamos caché del sistema
                DatabaseManager.limpiar_cache_sistema()
                return nueva_maquina, "Máquina registrada correctamente"
            else:
                return None, "Error al guardar la máquina"
            
        except Exception as e:
            return None, f"Error al guardar la máquina: {str(e)}"
    
    def actualizar_maquina(self, datos_dict):
        # Actualiza datos de máquina existente
        # ESCRITURA: Invalidamos caché después de actualizar
        
        # Validación: código es obligatorio
        codigo = datos_dict.get("codigo_equipo")
        if not codigo or codigo.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        maquina_db = self._maquina_dao.buscar_por_codigo(codigo)
        if not maquina_db:
            return None, f"La máquina '{codigo}' no existe"
        
        # Validación: si se proporciona tipo, debe ser PC o IMP
        tipo = datos_dict.get("tipo_equipo", "").upper()
        
        if tipo and tipo not in ["PC", "IMP"]:
            return None, "El tipo de equipo debe ser exactamente PC o IMP"
        
        # Si no se proporciona tipo, usamos el existente
        if not tipo:
            tipo = maquina_db.get('tipo', '').upper()
            # Normalizamos tipo existente para compatibilidad
            if tipo in ["COMPUTADORA"]:
                tipo = "PC"
            elif tipo in ["IMPRESORA"]:
                tipo = "IMP"
            elif tipo not in ["PC", "IMP"]:
                return None, "El tipo de equipo existente debe ser PC o IMP"
        
        # Obtenemos datos (nuevos o existentes)
        estado = datos_dict.get("estado_actual") or maquina_db.get('estado')
        area = datos_dict.get("area") or maquina_db.get('area')
        
        # Manejo de fecha opcional
        fecha_str = datos_dict.get("fecha") or maquina_db.get('fecha')
        fecha_obj = None
        
        if fecha_str and fecha_str.strip():
            try:
                from datetime import datetime
                if isinstance(fecha_str, str):
                    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                else:
                    fecha_obj = fecha_str
            except (ValueError, TypeError):
                fecha_obj = None
        
        usuario = datos_dict.get("usuario") or maquina_db.get('usuario')
        if usuario and not usuario.strip():
            usuario = None
        
        # Creamos objeto máquina actualizado
        try:
            if tipo == "PC":
                maquina_obj = Computadora(codigo, estado, area, fecha_obj, usuario)
            elif tipo == "IMP":
                maquina_obj = Impresora(codigo, estado, area, fecha_obj, usuario)
            
            # Actualizamos en base de datos
            resultado = self._maquina_dao.actualizar(maquina_obj)
            
            if resultado:
                # ESCRITURA: Invalidamos caché del sistema
                DatabaseManager.limpiar_cache_sistema()
                return maquina_obj, "Máquina actualizada correctamente"
            else:
                return None, "Error al actualizar la máquina"
                
        except Exception as e:
            return None, f"Error al actualizar la máquina: {str(e)}"
    
    def eliminar_maquina(self, codigo):
        # Elimina máquina del sistema
        # ESCRITURA: Invalidamos caché después de eliminar
        
        # Validación: código es obligatorio
        if not codigo or codigo.strip() == "":
            return False, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        if not self._maquina_dao.buscar_por_codigo(codigo):
            return False, f"La máquina '{codigo}' no existe"
        
        # Eliminamos la máquina
        if self._maquina_dao.eliminar(codigo):
            # ESCRITURA: Invalidamos caché del sistema
            DatabaseManager.limpiar_cache_sistema()
            return True, "Máquina eliminada correctamente"
        else:
            return False, "Error al eliminar la máquina"
    
    def obtener_maquina(self, codigo):
        # Obtiene datos de una máquina
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        # Validación: código es obligatorio
        if not codigo or codigo.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # LECTURA: Antes de ir al DAO, pedimos cliente Redis al DatabaseManager
        redis_cliente = DatabaseManager.get_redis()
        
        if redis_cliente is not None:
            # Intentamos obtener desde caché
            cache_key = f"maquina:{codigo.strip().lower()}"
            maquina_cache = RedisConnection.obtener_cache(cache_key)
            
            if maquina_cache is not None:
                return maquina_cache, None
        
        # Cache MISS o Redis no disponible: vamos al DAO
        maquina = self._maquina_dao.buscar_por_codigo(codigo)
        
        if maquina and redis_cliente is not None:
            # Guardamos en caché para próximas consultas
            cache_key = f"maquina:{codigo.strip().lower()}"
            RedisConnection.guardar_cache(cache_key, maquina, tiempo_vida=30)
        
        if maquina:
            return maquina, None
        else:
            return None, f"La máquina '{codigo}' no existe"
    
    def listar_todas_las_maquinas(self):
        # Obtiene todas las máquinas
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        # LECTURA: Antes de ir al DAO, pedimos cliente Redis al DatabaseManager
        redis_cliente = DatabaseManager.get_redis()
        
        if redis_cliente is not None:
            # Intentamos obtener desde caché
            maquinas_cache = RedisConnection.obtener_cache("cache:lista_maquinas")
            
            if maquinas_cache is not None:
                return maquinas_cache, None
        
        # Cache MISS o Redis no disponible: vamos al DAO
        try:
            maquinas = self._maquina_dao.listar_todas()
            
            if maquinas and redis_cliente is not None:
                # Guardamos en caché para próximas consultas
                RedisConnection.guardar_cache("cache:lista_maquinas", maquinas, tiempo_vida=30)
            
            return maquinas, None
        except Exception as e:
            return [], f"Error al listar máquinas: {str(e)}"
    
    def buscar_maquinas_por_codigo(self, codigo_parcial):
        # Busca máquinas por código parcial
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        try:
            # LECTURA: Antes de ir al DAO, pedimos cliente Redis al DatabaseManager
            redis_cliente = DatabaseManager.get_redis()
            
            if redis_cliente is not None:
                # Intentamos obtener desde caché
                cache_key = f"busqueda:codigo:{codigo_parcial or 'todos'}"
                resultado_cache = RedisConnection.obtener_cache(cache_key)
                
                if resultado_cache is not None:
                    return resultado_cache, None
            
            # Cache MISS o Redis no disponible: vamos al DAO
            todas_las_maquinas = self._maquina_dao.listar_todas()
            
            if not codigo_parcial:
                resultado = todas_las_maquinas
            else:
                # Filtramos máquinas que contienen el código parcial
                codigo_buscar = str(codigo_parcial).strip().lower()
                resultado = []
                
                for maquina in todas_las_maquinas:
                    codigo_maq = str(maquina.get("codigo", "")).lower()
                    if codigo_buscar in codigo_maq:
                        resultado.append(maquina)
            
            # Guardamos en caché si Redis está disponible
            if resultado and redis_cliente is not None:
                cache_key = f"busqueda:codigo:{codigo_parcial or 'todos'}"
                RedisConnection.guardar_cache(cache_key, resultado, tiempo_vida=30)
            
            return resultado, None
            
        except Exception as e:
            return [], f"Error al buscar máquinas: {str(e)}"
