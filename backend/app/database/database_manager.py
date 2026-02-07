# Encapsula operaciones de bases de datos
# Simplifica acceso a MySQL, MongoDB y Redis desde un solo lugar
# GERENTE DE DATOS: Centraliza todas las conexiones para la arquitectura

# Importamos clases que manejan conexiones
from app.database.mysql import MySQLConnection
from app.database.mongodb import MongoDB
from app.database.redis import RedisConnection

class DatabaseManager:
    # Contiene métodos estáticos para gestionar bases de datos
    # Es el GERENTE DE DATOS que centraliza todas las conexiones
    
    @staticmethod
    def inicializar():
        """Inicializa todas las bases de datos cuando arranca el servidor"""
        # Intentamos inicializar MySQL
        try:
            MySQLConnection.inicializar_base_datos()
        except Exception as e:
            print(f"Advertencia MySQL: {e}")
        
        # Intentamos conectar a MongoDB
        try:
            MongoDB.conectar()
        except Exception as e:
            print(f"Advertencia MongoDB: {e}")
        
        # Intentamos conectar a Redis
        try:
            redis_cliente = RedisConnection.conectar()
            if redis_cliente:
                print("Conexión a Redis establecida para caché")
            else:
                print("Redis no disponible - funcionando sin caché")
        except Exception as e:
            print(f"Advertencia Redis: {e}")
    
    @staticmethod
    def cerrar():
        """Cierra todas las conexiones cuando se apaga el servidor"""
        # Cerramos conexión a MongoDB
        MongoDB.cerrar()
        
        # Cerramos conexión a Redis
        RedisConnection.cerrar()
    
    @staticmethod
    def get_mysql_connection():
        """Obtiene conexión a MySQL para los DAOs"""
        return MySQLConnection.conectar()
    
    @staticmethod
    def get_redis():
        """Obtiene cliente Redis para los Services"""
        return RedisConnection.conectar()
    
    @staticmethod
    def limpiar_cache_sistema():
        """Borra claves de caché principales del sistema"""
        try:
            redis_cliente = RedisConnection.conectar()
            if redis_cliente is None:
                print("Redis no disponible - no se puede limpiar caché")
                return False
            
            # Eliminamos claves principales de caché
            claves_eliminadas = 0
            
            # Borramos cache:dashboard
            if RedisConnection.eliminar_cache("cache:dashboard"):
                claves_eliminadas += 1
                print("Caché 'cache:dashboard' eliminado")
            
            # Borramos cache:lista_maquinas
            if RedisConnection.eliminar_cache("cache:lista_maquinas"):
                claves_eliminadas += 1
                print("Caché 'cache:lista_maquinas' eliminado")
            
            # Borramos cache de reportes (informe:*)
            claves_reportes = RedisConnection.limpiar_patron("informe:*")
            claves_eliminadas += len(claves_reportes)
            print(f"Caché de reportes eliminado: {len(claves_reportes)} claves")
            
            # Borramos cache de mantenimientos (mantenimiento:*)
            claves_mantenimientos = RedisConnection.limpiar_patron("mantenimiento:*")
            claves_eliminadas += len(claves_mantenimientos)
            print(f"Caché de mantenimientos eliminado: {len(claves_mantenimientos)} claves")
            
            # Borramos cache de historial específico (historial:*)
            claves_historial = RedisConnection.limpiar_patron("historial:*")
            claves_eliminadas += len(claves_historial)
            print(f"Caché de historial eliminado: {len(claves_historial)} claves")
            
            # Limpiamos cualquier otra clave relacionada
            claves_adicionales = RedisConnection.limpiar_patron("cache:*")
            claves_eliminadas += claves_adicionales
            
            print(f"Se eliminaron {claves_eliminadas} claves de caché del sistema")
            return True
            
        except Exception as e:
            print(f"Error al limpiar caché del sistema: {e}")
            return False
    
    # Métodos legacy para compatibilidad
    @staticmethod
    def obtener_mysql():
        """Método legacy - usar get_mysql_connection()"""
        return DatabaseManager.get_mysql_connection()
    
    @staticmethod
    def obtener_mongodb():
        """Método legacy - retorna MongoDB para compatibilidad"""
        return MongoDB.conectar()
