# Este archivo centraliza todos los DAOs del sistema
# Repository funciona como un contenedor global de todos los objetos de acceso a datos

# Importamos todas las clases DAO que necesitamos
from app.daos.usuario_dao import UsuarioDAO
from app.daos.maquina_dao import MaquinaDAO
from app.daos.mantenimiento_dao import MantenimientoDAO

class ProyectoRepository:
    # Esta clase es el contenedor central de todos los DAOs
    
    def __init__(self):
        # En el constructor creamos una instancia de cada DAO
        # Estos objetos son los que se comunican directamente con la base de datos
        
        # DAO para operaciones con usuarios
        self.usuario_dao = UsuarioDAO()
        
        # DAO para operaciones con máquinas (PC e IMP)
        self.maquina_dao = MaquinaDAO()
        
        # DAO para operaciones con mantenimientos
        self.mantenimiento_dao = MantenimientoDAO()
    
    # Métodos para obtener cada DAO específico
    def get_usuario_dao(self):
        # Retorna el DAO de usuarios
        return self.usuario_dao
    
    def get_maquina_dao(self):
        # Retorna el DAO de máquinas
        return self.maquina_dao
    
    def get_mantenimiento_dao(self):
        # Retorna el DAO de mantenimientos
        return self.mantenimiento_dao

# Creamos una instancia global del Repository
# Esta instancia será compartida por toda la aplicación
repo_instancia = ProyectoRepository()

# Función conveniente para obtener la instancia global desde cualquier lugar
def get_repository():
    # Retorna la instancia global del repository
    return repo_instancia
