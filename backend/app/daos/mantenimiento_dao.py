from app.database.mongodb import MongoDB

class MantenimientoDAO:
    def __init__(self):
        self.db = MongoDB.conectar()
        self.collection = self.db["mantenimientos"]

    def guardar(self, mantenimiento):
        doc = {
            "codigo_maquina": mantenimiento.codigo_maquina_vinculada,
            "empresa": mantenimiento.empresa,
            "tecnico": mantenimiento.tecnico,
            "tipo": mantenimiento.tipo,
            "fecha": str(mantenimiento.fecha),
            "observaciones": mantenimiento.observaciones
        }
        self.collection.insert_one(doc)

    def listar_por_maquina(self, codigo_maquina):
        return list(self.collection.find({"codigo_maquina": codigo_maquina}))