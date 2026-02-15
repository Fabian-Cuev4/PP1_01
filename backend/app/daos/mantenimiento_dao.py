# DAO LIMPIO - Solo acceso a datos MongoDB
# Responsabilidades: consultas MongoDB puras, sin lógica de negocio

from app.database.mongodb import MongoDB

class MantenimientoDAO:
    def __init__(self):
        self.db = MongoDB.conectar()
        self.collection = self.db["mantenimientos"]

    # Inserta un mantenimiento con datos primitivos
    def insertar(self, codigo_maquina: str, empresa: str, tecnico: str, 
                 tipo: str, fecha: str, observaciones: str, usuario: str = None) -> bool:
        try:
            documento = {
                "codigo_maquina": codigo_maquina,
                "empresa": empresa,
                "tecnico": tecnico,
                "tipo": tipo,
                "fecha": fecha,
                "observaciones": observaciones,
                "usuario": usuario
            }
            self.collection.insert_one(documento)
            return True
        except Exception:
            return False

    # Elimina mantenimientos por código de máquina exacto
    def eliminar_por_maquina(self, codigo_maquina: str) -> int:
        try:
            resultado = self.collection.delete_many({"codigo_maquina": codigo_maquina})
            return resultado.deleted_count
        except Exception:
            return 0

    # Obtiene mantenimientos por código de máquina (sin ordenar)
    def listar_por_maquina(self, codigo: str) -> list:
        try:
            query = {"codigo_maquina": codigo}
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception:
            return []

    # Obtiene todos los mantenimientos (sin ordenar)
    def listar_todos(self) -> list:
        try:
            cursor = self.collection.find()
            return list(cursor)
        except Exception:
            return []

    # Obtiene mantenimientos ordenados por fecha
    def listar_por_maquina_ordenados(self, codigo: str, orden: int = -1) -> list:
        try:
            query = {"codigo_maquina": codigo}
            cursor = self.collection.find(query).sort("fecha", orden)
            return list(cursor)
        except Exception:
            return []

    # Busca mantenimientos por filtros múltiples
    def buscar_con_filtros(self, filtros: dict) -> list:
        try:
            cursor = self.collection.find(filtros)
            return list(cursor)
        except Exception:
            return []
