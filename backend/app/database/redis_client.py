import redis
import json

class RedisClient:
    _cliente = None

    @classmethod
    def conectar(cls):
        if cls._cliente is None:
            try:
                # Conectamos al contenedor llamado 'redis' (definido en docker-compose)
                cls._cliente = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
                # Probamos la conexión
                cls._cliente.ping()
                print(" Conexión exitosa a Redis")
            except Exception as e:
                print(f" Error conectando a Redis: {e}")
                cls._cliente = None
        return cls._cliente

    @classmethod
    def get(cls, key):
        if cls._cliente:
            try:
                data = cls._cliente.get(key)
                return json.loads(data) if data else None
            except Exception:
                return None
        return None

    @classmethod
    def set(cls, key, value, expire=5):
        """Guarda datos con un tiempo de vida (expire) en segundos"""
        if cls._cliente:
            try:
                cls._cliente.setex(key, expire, json.dumps(value, default=str))
            except Exception as e:
                print(f"Error guardando en Redis: {e}")

    @classmethod
    def delete(cls, key):
        if cls._cliente:
            try:
                cls._cliente.delete(key)
            except Exception:
                pass