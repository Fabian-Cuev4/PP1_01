# Este archivo se encarga de guardar y buscar mantenimientos en la base de datos MongoDB
# DAO significa "Data Access Object" (Objeto de Acceso a Datos)

# Importamos la clase que maneja la conexión a MongoDB
from app.database.mongodb import MongoDB

class MantenimientoDAO:
    # El constructor se ejecuta cuando creamos un objeto de esta clase
    def __init__(self):
        # Obtenemos la conexión a MongoDB
        self.db = MongoDB.conectar()
        # Seleccionamos la colección (tabla) de mantenimientos
        self.collection = self.db["mantenimientos"]

    # Esta función guarda un mantenimiento en MongoDB
    def guardar(self, mantenimiento):
        try:
            # Convertimos el objeto mantenimiento a un diccionario
            documento = mantenimiento.to_dict()
            # Insertamos el documento en la colección de MongoDB
            self.collection.insert_one(documento)
        except Exception as e:
            pass

    # Esta función elimina todos los mantenimientos de una máquina
    def eliminar_por_maquina(self, codigo_maquina):
        try:
            # Buscamos y eliminamos todos los mantenimientos que tengan ese código de máquina
            resultado = self.collection.delete_many({"codigo_maquina": codigo_maquina})
            # Retornamos cuántos documentos se eliminaron
            return resultado.deleted_count
        except Exception as e:
            return 0

    # Esta función obtiene todos los mantenimientos de una máquina específica
    def listar_por_maquina(self, codigo):
        try:
            # Creamos un filtro para buscar solo los mantenimientos de esa máquina
            query = {"codigo_maquina": codigo}
            # Buscamos y ordenamos por fecha descendente (los más recientes primero)
            cursor = self.collection.find(query).sort("fecha", -1)
            # Convertimos el cursor a una lista y la retornamos
            return list(cursor)
        except Exception as e:
            return []

    # Esta función obtiene todos los mantenimientos de todas las máquinas
    def listar_todos(self):
        try:
            # Buscamos todos los documentos en la colección (sin filtro)
            cursor = self.collection.find()
            # Convertimos el cursor a una lista y la retornamos
            return list(cursor)
        except Exception as e:
            return []
