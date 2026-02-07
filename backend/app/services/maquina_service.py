# Este archivo se encarga de la lógica de negocio de máquinas
# Service es el cerebro: aquí validamos y coordinamos las operaciones
# CAPA SERVICE: Antes de ir al DAO, pide el cliente Redis al Gerente.
# Si hay "Cache Hit", devuelve los datos al Front.
# Escritura e Invalidación: Llama a DatabaseManager.limpiar_cache_sistema()

# Importamos las clases necesarias
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora
from app.database.database_manager import DatabaseManager
from app.database.redis import RedisConnection

class MaquinaService:
    # Esta clase coordina todas las operaciones de máquinas (PC e IMP)
    # Es el CEREBRO que maneja caché y coordina con el DAO
    
    def __init__(self, maquina_dao):
        # Guardamos la referencia al DAO para usarla después
        self._maquina_dao = maquina_dao
    
    def registrar_maquina(self, datos_dict):
        # Esta función registra una nueva máquina en el sistema
        # ESCRITURA: Invalidamos caché después de guardar
        
        print(f"DEBUG: registrar_maquina recibido: {datos_dict}")
        print(f"DEBUG: tipo_equipo: {datos_dict.get('tipo_equipo')}")
        print(f"DEBUG: codigo_equipo: {datos_dict.get('codigo_equipo')}")
        
        # Validación: el código es obligatorio
        codigo = datos_dict.get("codigo_equipo")
        if not codigo or codigo.strip() == "":
            print("DEBUG: Código vacío")
            return None, "El código de la máquina es obligatorio"
        
        # Validación: el código debe ser único
        maquina_existente = self._maquina_dao.buscar_por_codigo(codigo)
        if maquina_existente:
            return None, f"El código '{codigo}' ya existe"
        
        # Validación: el tipo es obligatorio y debe ser exactamente PC o IMP
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
        fecha_obj = None  # Por defecto None si no hay fecha
        
        if fecha_str:  # Solo procesar si hay una fecha válida
            try:
                from datetime import datetime
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                return None, f"Formato de fecha inválido: {fecha_str}. Use YYYY-MM-DD"
        
        # Manejo de usuario opcional
        usuario_str = datos_dict.get("usuario", "").strip()
        if not usuario_str:
            usuario_str = None
        
        # Creamos el objeto máquina según su tipo (sin normalización)
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
            
            # Guardamos la máquina en la base de datos
            resultado = self._maquina_dao.guardar(nueva_maquina)
            print(f"DEBUG: Resultado de guardar: {resultado}")
            
            if resultado:
                # ESCRITURA: Invalidamos el caché del sistema
                print("DEBUG: Invalidando caché después de registrar máquina")
                DatabaseManager.limpiar_cache_sistema()
                
                return nueva_maquina, "Máquina registrada correctamente"
            else:
                return None, "Error al guardar la máquina"
            
        except Exception as e:
            return None, f"Error al guardar la máquina: {str(e)}"
    
    def actualizar_maquina(self, datos_dict):
        # Esta función actualiza los datos de una máquina existente
        # ESCRITURA: Invalidamos caché después de actualizar
        
        print(f"DEBUG: actualizar_maquina recibido: {datos_dict}")
        
        # Validación: el código es obligatorio
        codigo = datos_dict.get("codigo_equipo")
        if not codigo or codigo.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        maquina_db = self._maquina_dao.buscar_por_codigo(codigo)
        if not maquina_db:
            return None, f"La máquina '{codigo}' no existe"
        
        # Validación: si se proporciona tipo, debe ser exactamente PC o IMP
        tipo = datos_dict.get("tipo_equipo", "").upper()
        print(f"DEBUG: tipo recibido: {tipo}")
        
        if tipo and tipo not in ["PC", "IMP"]:
            print(f"DEBUG: tipo no válido: {tipo}")
            return None, "El tipo de equipo debe ser exactamente PC o IMP"
        
        # Si no se proporciona tipo, usamos el existente
        if not tipo:
            tipo = maquina_db.get('tipo', '').upper()
            print(f"DEBUG: tipo existente en DB: {tipo}")
            # Normalizamos el tipo existente para compatibilidad
            if tipo in ["COMPUTADORA"]:
                tipo = "PC"
            elif tipo in ["IMPRESORA"]:
                tipo = "IMP"
            elif tipo not in ["PC", "IMP"]:
                print(f"DEBUG: tipo existente no válido: {tipo}")
                return None, "El tipo de equipo existente debe ser PC o IMP"
        
        # Obtenemos los datos (nuevos o existentes)
        estado = datos_dict.get("estado_actual") or maquina_db.get('estado')
        area = datos_dict.get("area") or maquina_db.get('area')
        
        # Manejo de fecha opcional
        fecha_str = datos_dict.get("fecha") or maquina_db.get('fecha')
        fecha_obj = None
        
        if fecha_str and fecha_str.strip():  # Solo procesar si hay una fecha válida
            try:
                from datetime import datetime
                if isinstance(fecha_str, str):
                    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                else:
                    fecha_obj = fecha_str
            except (ValueError, TypeError):
                print(f"DEBUG: Error procesando fecha: {fecha_str}")
                fecha_obj = None
        
        usuario = datos_dict.get("usuario") or maquina_db.get('usuario')
        if usuario and not usuario.strip():
            usuario = None
        
        # Creamos el objeto máquina actualizado
        try:
            print(f"DEBUG: Creando objeto máquina con tipo: {tipo}")
            if tipo == "PC":
                maquina_obj = Computadora(codigo, estado, area, fecha_obj, usuario)
            elif tipo == "IMP":
                maquina_obj = Impresora(codigo, estado, area, fecha_obj, usuario)
            
            print(f"DEBUG: Objeto creado, actualizando en DB...")
            # Actualizamos en la base de datos
            resultado = self._maquina_dao.actualizar(maquina_obj)
            print(f"DEBUG: Resultado de actualización: {resultado}")
            
            if resultado:
                # ESCRITURA: Invalidamos el caché del sistema
                print("DEBUG: Invalidando caché después de actualizar máquina")
                DatabaseManager.limpiar_cache_sistema()
                
                return maquina_obj, "Máquina actualizada correctamente"
            else:
                return None, "Error al actualizar la máquina"
                
        except Exception as e:
            return None, f"Error al actualizar la máquina: {str(e)}"
    
    def eliminar_maquina(self, codigo):
        # Esta función elimina una máquina
        # ESCRITURA: Invalidamos caché después de eliminar
        
        # Validación: el código es obligatorio
        if not codigo or codigo.strip() == "":
            return False, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        if not self._maquina_dao.buscar_por_codigo(codigo):
            return False, f"La máquina '{codigo}' no existe"
        
        # Eliminamos la máquina
        if self._maquina_dao.eliminar(codigo):
            # ESCRITURA: Invalidamos el caché del sistema
            print("DEBUG: Invalidando caché después de eliminar máquina")
            DatabaseManager.limpiar_cache_sistema()
            
            return True, "Máquina eliminada correctamente"
        else:
            return False, "Error al eliminar la máquina"
    
    def obtener_maquina(self, codigo):
        # Esta función obtiene los datos de una máquina
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        # Validación: el código es obligatorio
        if not codigo or codigo.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # LECTURA: Antes de ir al DAO, pedimos el cliente Redis al Gerente
        redis_cliente = DatabaseManager.get_redis()
        
        if redis_cliente is not None:
            # Intentamos obtener desde caché
            cache_key = f"maquina:{codigo.strip().lower()}"
            maquina_cache = RedisConnection.obtener_cache(cache_key)
            
            if maquina_cache is not None:
                print(f"DEBUG: Cache HIT para máquina {codigo}")
                return maquina_cache, None
            else:
                print(f"DEBUG: Cache MISS para máquina {codigo}")
        else:
            print(f"DEBUG: Redis no disponible, yendo directamente a DAO para máquina {codigo}")
        
        # Cache MISS o Redis no disponible: vamos al DAO
        maquina = self._maquina_dao.buscar_por_codigo(codigo)
        
        if maquina and redis_cliente is not None:
                # Guardamos en caché para próximas consultas (optimizado para polling de 2s)
                cache_key = f"maquina:{codigo.strip().lower()}"
                RedisConnection.guardar_cache(cache_key, maquina, tiempo_vida=30)  # 30 segundos para sincronización rápida
                print(f"DEBUG: Guardado en caché máquina {codigo}")
        
        if maquina:
            return maquina, None
        else:
            return None, f"La máquina '{codigo}' no existe"
    
    def listar_todas_las_maquinas(self):
        # Esta función obtiene todas las máquinas
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        # LECTURA: Antes de ir al DAO, pedimos el cliente Redis al Gerente
        redis_cliente = DatabaseManager.get_redis()
        
        if redis_cliente is not None:
            # Intentamos obtener desde caché
            maquinas_cache = RedisConnection.obtener_cache("cache:lista_maquinas")
            
            if maquinas_cache is not None:
                print("DEBUG: Cache HIT para lista de máquinas")
                return maquinas_cache, None
            else:
                print("DEBUG: Cache MISS para lista de máquinas")
        else:
            print("DEBUG: Redis no disponible, yendo directamente a DAO para lista de máquinas")
        
        # Cache MISS o Redis no disponible: vamos al DAO
        try:
            maquinas = self._maquina_dao.listar_todas()
            
            if maquinas and redis_cliente is not None:
                # Guardamos en caché para próximas consultas (optimizado para polling de 2s)
                RedisConnection.guardar_cache("cache:lista_maquinas", maquinas, tiempo_vida=30)  # 30 segundos para sincronización rápida
                print("DEBUG: Guardado en caché lista de máquinas")
            
            return maquinas, None
        except Exception as e:
            return [], f"Error al listar máquinas: {str(e)}"
    
    def buscar_maquinas_por_codigo(self, codigo_parcial):
        # Esta función busca máquinas por código parcial
        # LECTURA: Primero busca en caché, si no hay va al DAO
        
        try:
            # LECTURA: Antes de ir al DAO, pedimos el cliente Redis al Gerente
            redis_cliente = DatabaseManager.get_redis()
            
            if redis_cliente is not None:
                # Intentamos obtener desde caché
                cache_key = f"busqueda:codigo:{codigo_parcial or 'todos'}"
                resultado_cache = RedisConnection.obtener_cache(cache_key)
                
                if resultado_cache is not None:
                    print(f"DEBUG: Cache HIT para búsqueda código '{codigo_parcial}'")
                    return resultado_cache, None
                else:
                    print(f"DEBUG: Cache MISS para búsqueda código '{codigo_parcial}'")
            else:
                print(f"DEBUG: Redis no disponible, yendo directamente a DAO para búsqueda código '{codigo_parcial}'")
            
            # Cache MISS o Redis no disponible: vamos al DAO
            todas_las_maquinas = self._maquina_dao.listar_todas()
            
            if not codigo_parcial:
                resultado = todas_las_maquinas
            else:
                # Filtramos las máquinas que contienen el código parcial
                codigo_buscar = str(codigo_parcial).strip().lower()
                resultado = []
                
                for maquina in todas_las_maquinas:
                    codigo_maq = str(maquina.get("codigo", "")).lower()
                    if codigo_buscar in codigo_maq:
                        resultado.append(maquina)
            
            # Guardamos en caché si Redis está disponible (optimizado para polling de 2s)
            if resultado and redis_cliente is not None:
                cache_key = f"busqueda:codigo:{codigo_parcial or 'todos'}"
                RedisConnection.guardar_cache(cache_key, resultado, tiempo_vida=30)  # 30 segundos para sincronización rápida
                print(f"DEBUG: Guardado en caché búsqueda código '{codigo_parcial}'")
            
            return resultado, None
            
        except Exception as e:
            return [], f"Error al buscar máquinas: {str(e)}"
