from pymongo import MongoClient
import os

class MongoDB:
    _client = None
    _db = None

    @classmethod
    def conectar(cls):
        if cls._client is None:
            # Aquí va la URL. Luego la cambiaremos por una variable de entorno para Docker
            uri = "mongodb://localhost:27017/"
            cls._client = MongoClient(uri)
            cls._db = cls._client["siglab_db"]
            print("¡Conexión a MongoDB establecida con éxito! :V")
        return cls._db

    @classmethod
    def cerrar(cls):
        if cls._client:
            cls._client.close()
            cls._client = None