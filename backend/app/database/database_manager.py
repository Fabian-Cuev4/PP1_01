# Este archivo encapsula (envuelve) todas las operaciones de bases de datos
from app.database.mysql import MySQLConnection
from app.database.mongodb import MongoDB
from app.database.redis_client import RedisClient  # <--- IMPORTAMOS REDIS

class DatabaseManager:
    
    @staticmethod
    def inicializar():
        print("--- Iniciando Servicios de Base de Datos ---")
        # 1. MySQL
        try:
            MySQLConnection.inicializar_base_datos()
        except Exception as e:
            print(f"Advertencia MySQL: {e}")
        
        # 2. MongoDB
        try:
            MongoDB.conectar()
        except Exception as e:
            print(f"Advertencia MongoDB: {e}")

        # 3. Redis (NUEVO)
        try:
            RedisClient.conectar()
        except Exception as e:
            print(f"Advertencia Redis: {e}")
    
    @staticmethod
    def cerrar():
        MongoDB.cerrar()
        # Redis maneja su propio pool, no es crítico cerrarlo explícitamente aquí
    
    @staticmethod
    def obtener_mysql():
        return MySQLConnection.conectar()
    
    @staticmethod
    def obtener_mongodb():
        return MongoDB.conectar()
    
    @staticmethod
    def obtener_redis():
        return RedisClient