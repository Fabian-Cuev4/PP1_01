# Este archivo encapsula (envuelve) todas las operaciones de bases de datos
# Simplifica el acceso a MySQL y MongoDB desde un solo lugar

# Importamos las clases que manejan las conexiones
from app.database.mysql import MySQLConnection
from app.database.mongodb import MongoDB

class DatabaseManager:
    # Esta clase contiene métodos estáticos para gestionar las bases de datos
    
    # Este método inicializa todas las bases de datos cuando arranca el servidor
    @staticmethod
    def inicializar():
        # Intentamos inicializar MySQL
        try:
            MySQLConnection.inicializar_base_datos()
        except Exception as e:
            # Si hay un error, lo imprimimos pero no detenemos el servidor
            print(f"Advertencia MySQL: {e}")
        
        # Intentamos conectar a MongoDB
        try:
            MongoDB.conectar()
        except Exception as e:
            # Si hay un error, lo imprimimos pero no detenemos el servidor
            print(f"Advertencia MongoDB: {e}")
    
    # Este método cierra todas las conexiones cuando se apaga el servidor
    @staticmethod
    def cerrar():
        # Cerramos la conexión a MongoDB
        MongoDB.cerrar()
    
    # Este método obtiene una conexión a MySQL
    @staticmethod
    def obtener_mysql():
        # Retornamos una conexión a MySQL
        return MySQLConnection.conectar()
    
    # Este método obtiene la base de datos MongoDB
    @staticmethod
    def obtener_mongodb():
        # Retornamos la base de datos MongoDB
        return MongoDB.conectar()
