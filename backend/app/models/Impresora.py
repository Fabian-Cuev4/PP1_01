from app.models.abstrac_factory.Maquina import Maquina

# Representa una impresora del espacio de trabajo
class Impresora(Maquina):
    def __init__(self, codigo_equipo, estado_actual, area, fecha, usuario=None):
        super().__init__(codigo_equipo, "Impresora", estado_actual, area, fecha, usuario)