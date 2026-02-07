# Este archivo se encarga de guardar y buscar mantenimientos en la base de datos MongoDB
# DAO significa "Data Access Object" (Objeto de Acceso a Datos)
# Su única función es ejecutar operaciones de base de datos, sin lógica de negocio
# CAPA DAO: Solo usa el Gerente para pedir conexiones. No sabe que existe Redis.

# Importamos el GERENTE DE DATOS para obtener conexiones
from app.database.database_manager import DatabaseManager

class MantenimientoDAO:
    # El constructor se ejecuta cuando creamos un objeto de esta clase
    def __init__(self):
        # Obtenemos la conexión a MongoDB usando el GERENTE DE DATOS
        # Los DAOs SOLO usan el Gerente, no saben que existe Redis
        self.db = DatabaseManager.obtener_mongodb()
        # Seleccionamos la colección (tabla) de mantenimientos
        self.collection = self.db["mantenimientos"]

    # Esta función guarda un mantenimiento en MongoDB
    # Recibe un objeto mantenimiento con todos los datos listos para guardar
    def guardar(self, mantenimiento):
        try:
            # Convertimos el objeto mantenimiento a un diccionario
            documento = mantenimiento.to_dict()
            # Insertamos el documento en la colección de MongoDB
            self.collection.insert_one(documento)
            # Retornamos True para indicar éxito
            return True
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos False
            print(f"Error al guardar mantenimiento: {e}")
            return False

    # Esta función elimina todos los mantenimientos de una máquina
    # Recibe el código de la máquina y retorna la cantidad eliminada
    def eliminar_por_maquina(self, codigo_maquina):
        try:
            # Buscamos y eliminamos todos los mantenimientos que tengan ese código de máquina
            resultado = self.collection.delete_many({"codigo_maquina": codigo_maquina})
            # Retornamos cuántos documentos se eliminaron
            return resultado.deleted_count
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos 0
            print(f"Error al eliminar mantenimientos: {e}")
            return 0

    # Esta función obtiene todos los mantenimientos de una máquina específica
    # Recibe el código de la máquina y retorna una lista de mantenimientos
    def listar_por_maquina(self, codigo):
        try:
            # Creamos un filtro para buscar solo los mantenimientos de esa máquina
            query = {"codigo_maquina": codigo}
            # Buscamos y ordenamos por fecha descendente (los más recientes primero)
            cursor = self.collection.find(query).sort("fecha", -1)
            # Convertimos el cursor a una lista y la retornamos
            return list(cursor)
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos una lista vacía
            print(f"Error al buscar historial: {e}")
            return []

    # Esta función obtiene todos los mantenimientos de todas las máquinas
    # Retorna una lista con todos los mantenimientos del sistema
    def listar_todos(self):
        try:
            # Buscamos todos los documentos en la colección (sin filtro)
            cursor = self.collection.find()
            # Convertimos el cursor a una lista y la retornamos
            return list(cursor)
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos una lista vacía
            print(f"Error al listar mantenimientos: {e}")
            return []
