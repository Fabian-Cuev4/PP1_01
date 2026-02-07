# Centraliza todos los DAOs del sistema
# Repository funciona como contenedor global de objetos de acceso a datos

# Importamos todas las clases DAO necesarias
from app.daos.usuario_dao import UsuarioDAO
from app.daos.maquina_dao import MaquinaDAO
from app.daos.mantenimiento_dao import MantenimientoDAO

class ProyectoRepository:
    # Contenedor central de todos los DAOs
    
    def __init__(self):
        # Creamos instancia de cada DAO
        # Estos objetos se comunican directamente con base de datos
        
        # DAO para operaciones con usuarios
        self.usuario_dao = UsuarioDAO()
        
        # DAO para operaciones con máquinas (PC e IMP)
        self.maquina_dao = MaquinaDAO()
        
        # DAO para operaciones con mantenimientos
        self.mantenimiento_dao = MantenimientoDAO()
    
    # Métodos para obtener cada DAO específico
    def get_usuario_dao(self):
        return self.usuario_dao
    
    def get_maquina_dao(self):
        return self.maquina_dao
    
    def get_mantenimiento_dao(self):
        return self.mantenimiento_dao

# Instancia global del Repository
# Compartida por toda la aplicación
repo_instancia = ProyectoRepository()

# Función conveniente para obtener instancia global
def get_repository():
    return repo_instancia
