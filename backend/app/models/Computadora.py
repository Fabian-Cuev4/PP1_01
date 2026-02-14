from app.models.abstrac_factory.Maquina import Maquina

# Representa una computadora del espacio de trabajo
class Computadora(Maquina):
    def __init__(self, codigo_equipo, estado_actual, area, fecha, usuario=None):
        super().__init__(codigo_equipo, "Computadora", estado_actual, area, fecha, usuario)
    
    def obtener_tipo_especifico(self):
        """Retorna el tipo específico de computadora"""
        return "PC"
    
    def validar_datos(self):
        """Valida datos específicos de computadora"""
        if not self.codigo_equipo or not self.codigo_equipo.strip():
            raise ValueError("El código de la computadora es requerido")
        if not self.area or not self.area.strip():
            raise ValueError("El área de la computadora es requerida")
        return True