from abc import ABC, abstractmethod
from datetime import datetime

# Clase base para todas las personas del sistema
class Persona(ABC):
    def __init__(self, nombre_completo, tipo_persona, fecha_registro=None):
        self.nombre_completo = nombre_completo
        self.tipo_persona = tipo_persona
        self.fecha_registro = fecha_registro or datetime.now()
    
    @abstractmethod
    def obtener_tipo_especifico(self):
        # Método abstracto que debe implementar cada tipo de persona
        pass
    
    @abstractmethod
    def validar_datos(self):
        # Método abstracto para validar datos específicos del tipo
        pass
    
    def to_dict(self):
        # Convierte la persona a diccionario para guardar en BD
        return {
            "nombre_completo": self.nombre_completo,
            "tipo_persona": self.tipo_persona,
            "fecha_registro": self.fecha_registro
        }
