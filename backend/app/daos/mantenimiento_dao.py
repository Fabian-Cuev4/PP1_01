# Este archivo es el DAO para los Mantenimientos.
# A diferencia de los otros, este usa MongoDB porque los registros pueden ser muy variados.

from app.database.mongodb import MongoDB

class MantenimientoDAO:
    
    def __init__(self):
        # Nos conectamos a la base de datos de MongoDB usando nuestra clase personalizada
        self.db = MongoDB.conectar()
        # Seleccionamos la colección (tabla en Mongo) de 'mantenimientos'
        self.collection = self.db["mantenimientos"]

    def guardar(self, mantenimiento):
        
        #Recibe un objeto mantenimiento y lo guarda como un documento en MongoDB.
        
        try:
            # Usamos el método to_dict del objeto mantenimiento para obtener los datos limpiamente
            documento = mantenimiento.to_dict()
            
            # Insertamos el documento en la base de datos Mongo
            self.collection.insert_one(documento)
            print(f"Mantenimiento guardado en MongoDB para el equipo: {mantenimiento.maquina.codigo_equipo}")
        except Exception as e:
            print(f"Error al guardar mantenimiento en MongoDB: {e}")

    def listar_por_maquina(self, codigo):
        
        #Busca todos los registros de mantenimiento de una máquina específica.
        try:
            # Buscamos en Mongo los documentos que tengan ese código de máquina
            # sorted by fecha descending (las más nuevas primero)
            query = {"codigo_maquina": codigo}
            cursor = self.collection.find(query).sort("fecha", -1)
            return list(cursor)
        except Exception as e:
            print(f"Error al buscar historial en Mongo: {e}")
            return []

    def listar_todos(self):
        
        #Trae todos los mantenimientos de todas las máquinas.
        
        try:
            # El find() vacío nos trae todo lo que hay en la colección
            cursor = self.collection.find()
            return list(cursor)
        except Exception as e:
            print(f"Error al traer todos los mantenimientos: {e}")
            return []
