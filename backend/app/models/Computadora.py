from app.models.abstrac_factory.Maquina import Maquina

class Computadora(Maquina):
    def __init__(self, codigo_equipo, estado_actual, area, fecha):
        super().__init__(
            codigo_equipo=codigo_equipo, 
            estado_actual=estado_actual, 
            area=area, 
            fecha=fecha,
            tipo_maquina="Computadora"
        )