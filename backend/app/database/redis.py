# Este archivo maneja la conexión a Redis para el sistema de caché
# Redis es una base de datos en memoria que usamos para caché y polling

import redis
import json
import os
from typing import Optional, Any

class RedisConnection:
    # Esta clase maneja toda la comunicación con Redis
    
    _cliente = None  # Variable estática para mantener una única conexión
    
    @classmethod
    def conectar(cls) -> Optional[redis.Redis]:
        """
        Este método establece la conexión a Redis
        Retorna el cliente de Redis o None si no hay conexión
        """
        try:
            # Si ya tenemos una conexión, la retornamos
            if cls._cliente is not None:
                return cls._cliente
            
            # Obtenemos la configuración desde variables de entorno
            redis_host = os.getenv("REDIS_HOST", "localhost")
            redis_port = int(os.getenv("REDIS_PORT", "6379"))
            redis_db = int(os.getenv("REDIS_DB", "0"))
            
            # Creamos la conexión a Redis
            cls._cliente = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                decode_responses=True,  # Para que los strings se decodifiquen automáticamente
                socket_connect_timeout=5,  # Timeout de 5 segundos para conectar
                socket_timeout=5,  # Timeout de 5 segundos para operaciones
                retry_on_timeout=True  # Reintentar si hay timeout
            )
            
            # Probamos la conexión con un ping
            cls._cliente.ping()
            print(f"Conexión a Redis establecida: {redis_host}:{redis_port}")
            return cls._cliente
            
        except Exception as e:
            print(f"Error al conectar a Redis: {e}")
            cls._cliente = None
            return None
    
    @classmethod
    def cerrar(cls):
        """
        Este método cierra la conexión a Redis
        """
        try:
            if cls._cliente is not None:
                cls._cliente.close()
                cls._cliente = None
                print("Conexión a Redis cerrada")
        except Exception as e:
            print(f"Error al cerrar Redis: {e}")
    
    @classmethod
    def esta_disponible(cls) -> bool:
        """
        Este método verifica si Redis está disponible
        Retorna True si hay conexión, False si no
        """
        try:
            if cls._cliente is None:
                return False
            # Hacemos un ping para verificar que la conexión está activa
            cls._cliente.ping()
            return True
        except:
            return False
    
    @classmethod
    def guardar_cache(cls, clave: str, datos: Any, tiempo_vida: int = 300) -> bool:
        """
        Este método guarda datos en caché
        
        Parámetros:
        - clave: identificador único para los datos
        - datos: información a guardar (se convierte a JSON)
        - tiempo_vida: segundos antes de que expire (default: 5 minutos)
        
        Retorna True si se guardó correctamente, False si no
        """
        try:
            cliente = cls.conectar()
            if cliente is None:
                return False
            
            # Convertimos los datos a JSON string
            datos_json = json.dumps(datos, default=str)
            
            # Guardamos en Redis con tiempo de vida
            cliente.setex(clave, tiempo_vida, datos_json)
            return True
            
        except Exception as e:
            print(f"Error al guardar en caché: {e}")
            return False
    
    @classmethod
    def obtener_cache(cls, clave: str) -> Optional[Any]:
        """
        Este método obtiene datos desde caché
        
        Parámetros:
        - clave: identificador único de los datos
        
        Retorna los datos si existen, None si no hay caché o hay error
        """
        try:
            cliente = cls.conectar()
            if cliente is None:
                return None
            
            # Obtenemos los datos desde Redis
            datos_json = cliente.get(clave)
            
            if datos_json is None:
                return None
            
            # Convertimos desde JSON
            return json.loads(datos_json)
            
        except Exception as e:
            print(f"Error al obtener desde caché: {e}")
            return None
    
    @classmethod
    def eliminar_cache(cls, clave: str) -> bool:
        """
        Este método elimina una clave específica de caché
        
        Parámetros:
        - clave: identificador único a eliminar
        
        Retorna True si se eliminó correctamente, False si no
        """
        try:
            cliente = cls.conectar()
            if cliente is None:
                return False
            
            # Eliminamos la clave
            resultado = cliente.delete(clave)
            return resultado > 0
            
        except Exception as e:
            print(f"Error al eliminar caché: {e}")
            return False
    
    @classmethod
    def limpiar_patron(cls, patron: str) -> int:
        """
        Este método elimina todas las claves que coinciden con un patrón
        
        Parámetros:
        - patron: patrón a buscar (ej: "cache:*")
        
        Retorna el número de claves eliminadas
        """
        try:
            cliente = cls.conectar()
            if cliente is None:
                return 0
            
            # Buscamos todas las claves con el patrón
            claves = cliente.keys(patron)
            
            if not claves:
                return 0
            
            # Eliminamos todas las claves encontradas
            eliminadas = cliente.delete(*claves)
            return eliminadas
            
        except Exception as e:
            print(f"Error al limpiar patrón de caché: {e}")
            return 0
