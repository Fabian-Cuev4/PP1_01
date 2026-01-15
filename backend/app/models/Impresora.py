# Importamos la clase base Maquina para poder heredar de ella
from app.models.abstrac_factory.Maquina import Maquina 

class Impresora(Maquina):
    def __init__(self, codigo_equipo, estado_actual, area, fecha):
        # super().__init__ envía los datos al constructor de Maquina
        super().__init__(
            codigo_equipo=codigo_equipo, 
            estado_actual=estado_actual, 
            area=area, 
            fecha=fecha,
            tipo_maquina="Impresora"
        )