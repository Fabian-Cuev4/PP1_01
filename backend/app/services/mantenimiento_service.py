# Lógica de negocio de mantenimientos
# Service es el cerebro: valida y coordina operaciones
# CAPA SERVICE: Antes de ir al DAO, pide cliente Redis al DatabaseManager
# Si hay "Cache Hit", devuelve datos al Front
# Escritura e Invalidación: Llama a DatabaseManager.limpiar_cache_sistema()

# Importamos clases necesarias
from app.models.Mantenimiento import Mantenimiento
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora
from app.database.database_manager import DatabaseManager
from app.database.redis import RedisConnection

class MantenimientoService:
    # Coordina todas las operaciones de mantenimientos
    # Es el CEREBRO que maneja caché y coordina con los DAOs
    
    def __init__(self, mantenimiento_dao, maquina_dao):
        # Guardamos referencias a los DAOs para uso posterior
        self._mantenimiento_dao = mantenimiento_dao
        self._maquina_dao = maquina_dao
    
    def registrar_mantenimiento(self, datos_dict):
        # Registra nuevo mantenimiento con todas las validaciones
        # ESCRITURA: Invalidamos caché después de guardar
        
        # Validación: código de máquina es obligatorio
        codigo_maquina = datos_dict.get("codigo_maquina")
        if not codigo_maquina or codigo_maquina.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        maquina_db = self._maquina_dao.buscar_por_codigo(codigo_maquina)
        if not maquina_db:
            return None, f"La máquina '{codigo_maquina}' no existe"
        
        # Validación: campos obligatorios
        if not datos_dict.get("empresa"):
            return None, "La empresa es obligatoria"
        
        if not datos_dict.get("tecnico"):
            return None, "El técnico es obligatorio"
        
        if not datos_dict.get("tipo"):
            return None, "El tipo de mantenimiento es obligatorio"
        
        if not datos_dict.get("fecha"):
            return None, "La fecha es obligatoria"
        
        if not datos_dict.get("usuario"):
            return None, "El usuario que registra es obligatorio"
        
        # Creamos objeto máquina según su tipo
        tipo_maquina = maquina_db.get('tipo', '').upper()
        if tipo_maquina in ['COMPUTADORA', 'PC']:
            maquina_obj = Computadora(
                maquina_db['codigo'],
                maquina_db['estado'],
                maquina_db['area'],
                maquina_db['fecha'],
                maquina_db.get('usuario')
            )
        elif tipo_maquina in ['IMPRESORA', 'IMP']:
            maquina_obj = Impresora(
                maquina_db['codigo'],
                maquina_db['estado'],
                maquina_db['area'],
                maquina_db['fecha'],
                maquina_db.get('usuario')
            )
        else:
            return None, "Tipo de máquina no reconocido"
        
        # Usamos usuario del mantenimiento o de la máquina
        usuario = datos_dict.get("usuario") or maquina_db.get('usuario')
        
        # Creamos objeto mantenimiento
        try:
            nuevo_mantenimiento = Mantenimiento(
                maquina_objeto=maquina_obj,
                empresa=datos_dict.get("empresa"),
                tecnico=datos_dict.get("tecnico"),
                tipo=datos_dict.get("tipo"),
                fecha=datos_dict.get("fecha"),
                observaciones=datos_dict.get("observaciones", ""),
                usuario=usuario
            )
            
            # Guardamos mantenimiento
            resultado = self._mantenimiento_dao.guardar(nuevo_mantenimiento)
            
            if resultado:
                # ESCRITURA: Invalidamos caché del sistema
                DatabaseManager.limpiar_cache_sistema()
                return nuevo_mantenimiento, "Mantenimiento registrado correctamente"
            else:
                return None, "Error al guardar el mantenimiento"
            
        except Exception as e:
            return None, f"Error al guardar el mantenimiento: {str(e)}"
    
    def obtener_historial_por_maquina(self, codigo_maquina):
        # Obtiene todos los mantenimientos de una máquina
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        # Validación: código es obligatorio
        if not codigo_maquina or codigo_maquina.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        if not self._maquina_dao.buscar_por_codigo(codigo_maquina):
            return None, f"La máquina '{codigo_maquina}' no existe"
        
        # LECTURA: Antes de ir al DAO, pedimos cliente Redis al DatabaseManager
        redis_cliente = DatabaseManager.get_redis()
        
        if redis_cliente is not None:
            # Intentamos obtener desde caché
            cache_key = f"historial:{codigo_maquina.strip().lower()}"
            historial_cache = RedisConnection.obtener_cache(cache_key)
            
            if historial_cache is not None:
                return historial_cache, None
        
        # Cache MISS o Redis no disponible: vamos al DAO
        try:
            historial = self._mantenimiento_dao.listar_por_maquina(codigo_maquina)
            
            if historial and redis_cliente is not None:
                # Guardamos en caché para próximas consultas
                cache_key = f"historial:{codigo_maquina.strip().lower()}"
                RedisConnection.guardar_cache(cache_key, historial, tiempo_vida=2)
            
            return historial, None
        except Exception as e:
            return None, f"Error al obtener el historial: {str(e)}"
    
    def obtener_todos_los_mantenimientos(self):
        # Obtiene todos los mantenimientos del sistema
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        # LECTURA: Antes de ir al DAO, pedimos cliente Redis al DatabaseManager
        redis_cliente = DatabaseManager.get_redis()
        
        if redis_cliente is not None:
            # Intentamos obtener desde caché
            mantenimientos_cache = RedisConnection.obtener_cache("cache:lista_mantenimientos")
            
            if mantenimientos_cache is not None:
                return mantenimientos_cache, None
        
        # Cache MISS o Redis no disponible: vamos al DAO
        try:
            mantenimientos = self._mantenimiento_dao.listar_todos()
            
            if mantenimientos and redis_cliente is not None:
                # Guardamos en caché para próximas consultas
                RedisConnection.guardar_cache("cache:lista_mantenimientos", mantenimientos, tiempo_vida=300)
            
            return mantenimientos, None
        except Exception as e:
            return [], f"Error al listar mantenimientos: {str(e)}"
    
    def eliminar_mantenimientos_por_maquina(self, codigo_maquina):
        # Elimina todos los mantenimientos de una máquina
        # ESCRITURA: Invalidamos caché después de eliminar
        
        # Validación: código es obligatorio
        if not codigo_maquina or codigo_maquina.strip() == "":
            return False, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        if not self._maquina_dao.buscar_por_codigo(codigo_maquina):
            return False, f"La máquina '{codigo_maquina}' no existe"
        
        # Eliminamos los mantenimientos
        try:
            cantidad_eliminada = self._mantenimiento_dao.eliminar_por_maquina(codigo_maquina)
            
            if cantidad_eliminada > 0:
                # ESCRITURA: Invalidamos caché del sistema
                DatabaseManager.limpiar_cache_sistema()
                return True, f"Se eliminaron {cantidad_eliminada} mantenimientos"
            else:
                return True, "No había mantenimientos que eliminar"
                
        except Exception as e:
            return False, f"Error al eliminar mantenimientos: {str(e)}"
    
    def obtener_informe_completo(self, codigo_maquina=None):
        # Genera reporte completo de máquinas y mantenimientos
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        try:
            # LECTURA: Antes de ir al DAO, pedimos cliente Redis al DatabaseManager
            redis_cliente = DatabaseManager.get_redis()
            
            if redis_cliente is not None:
                # Intentamos obtener desde caché
                cache_key = f"informe:{codigo_maquina or 'completo'}"
                informe_cache = RedisConnection.obtener_cache(cache_key)
                
                if informe_cache is not None:
                    return informe_cache, None
            
            # Cache MISS o Redis no disponible: vamos al DAO
            # Obtenemos todas las máquinas
            todas_las_maquinas = self._maquina_dao.listar_todas()
            
            # Si nos dieron un código, filtramos solo esa máquina
            if codigo_maquina:
                codigo_buscar = str(codigo_maquina).strip().lower()
                maquinas_filtradas = []
                for maquina in todas_las_maquinas:
                    codigo_maq = str(maquina.get("codigo", "")).lower()
                    if codigo_buscar in codigo_maq:
                        maquinas_filtradas.append(maquina)
                maquinas_db = maquinas_filtradas
            else:
                maquinas_db = todas_las_maquinas
            
            # Si no hay máquinas, retornamos lista vacía
            if not maquinas_db:
                resultado = []
                # Guardamos en caché si Redis está disponible
                if redis_cliente is not None:
                    cache_key = f"informe:{codigo_maquina or 'completo'}"
                    RedisConnection.guardar_cache(cache_key, resultado, tiempo_vida=30)
                return resultado, None
            
            # Obtenemos todos los mantenimientos
            todos_mantenimientos = self._mantenimiento_dao.listar_todos() or []
            
            # Agrupamos mantenimientos por código de máquina
            mantenimientos_por_maquina = {}
            for mantenimiento in todos_mantenimientos:
                codigo_mt = mantenimiento.get("codigo_maquina") or mantenimiento.get("codigo")
                if codigo_mt:
                    codigo_key = str(codigo_mt).strip().lower()
                    if codigo_key not in mantenimientos_por_maquina:
                        mantenimientos_por_maquina[codigo_key] = []
                    
                    # Convertimos ID de MongoDB a string
                    if "_id" in mantenimiento:
                        mantenimiento["_id"] = str(mantenimiento["_id"])
                    
                    # Si no tiene tipo, le ponemos "N/A"
                    if "tipo" not in mantenimiento:
                        mantenimiento["tipo"] = "N/A"
                    
                    mantenimientos_por_maquina[codigo_key].append(mantenimiento)
            
            # Construimos reporte final
            resultado = []
            for maquina in maquinas_db:
                codigo_maq = str(maquina.get("codigo", "")).strip().lower()
                mantenimientos = mantenimientos_por_maquina.get(codigo_maq, [])
                
                resultado.append({
                    "codigo": maquina["codigo"],
                    "tipo": maquina["tipo"],
                    "area": maquina["area"],
                    "estado": maquina["estado"],
                    "mantenimientos": mantenimientos
                })
            
            # Guardamos en caché si Redis está disponible
            if resultado and redis_cliente is not None:
                cache_key = f"informe:{codigo_maquina or 'completo'}"
                RedisConnection.guardar_cache(cache_key, resultado, tiempo_vida=180)
            
            return resultado, None
            
        except Exception as e:
            return [], f"Error al generar informe: {str(e)}"
