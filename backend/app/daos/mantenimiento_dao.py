from app.database.mongodb import MongoDB

class MantenimientoDAO:
    def __init__(self):
        # Conexión a la base de datos a través de la clase global
        self.db = MongoDB.conectar()
        self.collection = self.db["mantenimientos"]

    def guardar(self, mantenimiento):
        """Guarda un nuevo registro en la colección de MongoDB"""
        doc = {
            "codigo_maquina": mantenimiento.codigo_maquina_vinculada,
            "empresa": mantenimiento.empresa,
            "tecnico": mantenimiento.tecnico,
            "tipo": mantenimiento.tipo,
            "fecha": str(mantenimiento.fecha),
            "observaciones": mantenimiento.observaciones,
            "tipo_maquina": mantenimiento.maquina_objeto.tipo_maquina
        }
        resultado = self.collection.insert_one(doc)
        return str(resultado.inserted_id)

    def listar_por_maquina(self, codigo_maquina):
        """Filtra en MongoDB todos los mantenimientos de una máquina específica"""
        cursor = self.collection.find({"codigo_maquina": codigo_maquina})
        return list(cursor)