from abc import ABC, abstractmethod

# Clase base para todas las máquinas del laboratorio
class Maquina(ABC):
    def __init__(self, codigo_equipo, tipo_equipo, estado_actual, area, fecha, usuario=None):
        self.codigo_equipo = codigo_equipo
        self.tipo_equipo = tipo_equipo
        self.estado_actual = estado_actual
        self.area = area
        self.fecha = fecha
        self.usuario = usuario  # Usuario asociado a la máquina
    
    @abstractmethod
    def obtener_tipo_especifico(self):
        # Método abstracto que debe implementar cada tipo de máquina
        pass
    
    @abstractmethod
    def validar_datos(self):
        # Método abstracto para validar datos específicos del tipo
        pass
    
    def to_dict(self):
        # Convierte la máquina a diccionario para guardar en BD
        return {
            "codigo_equipo": self.codigo_equipo,
            "tipo_equipo": self.tipo_equipo,
            "estado_actual": self.estado_actual,
            "area": self.area,
            "fecha": self.fecha,
            "usuario": self.usuario
        }