from pymongo import MongoClient
import os

class MongoDB:
    _client = None
    _db = None

    @classmethod
    def conectar(cls):
        if cls._client is None:
            import time
            max_retries = 5
            retry_delay = 2
            
            # Usar variable de entorno para Docker, con fallback a localhost
            mongo_host = os.getenv('MONGO_HOST', 'mongodb')
            mongo_port = os.getenv('MONGO_PORT', '27017')
            uri = f"mongodb://{mongo_host}:{mongo_port}/"
            
            for attempt in range(max_retries):
                try:
                    cls._client = MongoClient(uri, serverSelectionTimeoutMS=5000)
                    # Verificar conexión
                    cls._client.admin.command('ping')
                    cls._db = cls._client["siglab_db"]
                    print("¡Conexión a MongoDB establecida con éxito! :V")
                    return cls._db
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"Intento {attempt + 1}/{max_retries} de conexión a MongoDB fallido. Reintentando en {retry_delay} segundos... Error: {e}")
                        time.sleep(retry_delay)
                    else:
                        print(f"ERROR: No se pudo conectar a MongoDB después de {max_retries} intentos: {e}")
                        raise
        return cls._db

    @classmethod
    def cerrar(cls):
        if cls._client:
            cls._client.close()
            cls._client = None