from app.models.abstrac_factory.Maquina import Maquina

# Representa una impresora del espacio de trabajo
class Impresora(Maquina):
    def __init__(self, codigo_equipo, tipo_equipo, estado_actual, area, fecha, usuario=None):
        super().__init__(codigo_equipo, tipo_equipo, estado_actual, area, fecha, usuario)
    
    def obtener_tipo_especifico(self):
        # Retorna el tipo específico de impresora
        return "IMP"
    
    def validar_datos(self):
        # Valida datos específicos de impresora
        if not self.codigo_equipo or not self.codigo_equipo.strip():
            raise ValueError("El código de la impresora es requerido")
        if not self.area or not self.area.strip():
            raise ValueError("El área de la impresora es requerida")
        return True