from app.models.abstrac_factory.Maquina import Maquina

# Modelo que representa una computadora del espacio de trabajo
class Computadora(Maquina):
    def __init__(self, codigo_equipo, estado_actual, area, fecha, usuario=None):
        super().__init__(codigo_equipo, "Computadora", estado_actual, area, fecha, usuario)