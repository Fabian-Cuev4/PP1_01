# Este archivo crea los objetos que acceden a las bases de datos
# Es como un "repositorio" que guarda todas las herramientas para trabajar con datos

# Importamos las clases DAO (Data Access Objects)
from app.daos.maquina_dao import MaquinaDAO
from app.daos.mantenimiento_dao import MantenimientoDAO

class ProyectoRepository:
    # El constructor se ejecuta cuando creamos un objeto de esta clase
    def __init__(self):
        # Creamos un objeto para acceder a la tabla de máquinas
        self.maquina_dao = MaquinaDAO()
        # Creamos un objeto para acceder a la tabla de mantenimientos
        self.mantenimiento_dao = MantenimientoDAO()

# Creamos una instancia global del repositorio
# Esto significa que se crea una sola vez y se puede usar en todo el proyecto
repo_instancia = ProyectoRepository()
