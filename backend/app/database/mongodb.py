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
            
            # EXPLICACIÓN: Usar variable de entorno para Docker, con fallback a localhost
            mongo_host = os.getenv('MONGO_HOST', 'mongo_db')  # EXPLICACIÓN: Actualizado para Docker
            mongo_port = os.getenv('MONGO_PORT', '27017')
            uri = f"mongodb://{mongo_host}:{mongo_port}/"
            
            for attempt in range(max_retries):
                try:
                    # EXPLICACIÓN: Log de intento de conexión al archivador central MongoDB
                    print(f"🔌 Intentando conectar al archivador central MongoDB (intento {attempt + 1}/{max_retries})...")
                    
                    # Configurar pool de conexiones para reutilizar conexiones
                    cls._client = MongoClient(
                        uri, 
                        serverSelectionTimeoutMS=5000,
                        maxPoolSize=10,  # Máximo de conexiones en el pool
                        minPoolSize=1,    # Mínimo de conexiones en el pool
                        maxIdleTimeMS=45000  # Cerrar conexiones inactivas después de 45s
                    )
                    # Verificar conexión
                    cls._client.admin.command('ping')
                    cls._db = cls._client["siglab_db"]
                    print("✅ ¡Conectado exitosamente al archivador central (MongoDB)!")
                    return cls._db
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"❌ Intento {attempt + 1}/{max_retries} de conexión a MongoDB fallido. Reintentando en {retry_delay} segundos... Error: {e}")
                        time.sleep(retry_delay)
                    else:
                        print(f"🚫 ERROR: No se pudo conectar al archivador central MongoDB después de {max_retries} intentos: {e}")
                        raise
        return cls._db

    @classmethod
    def cerrar(cls):
        if cls._client:
            cls._client.close()
            cls._client = None