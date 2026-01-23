from abc import ABC

# Esta es la base (molde) de cualquier máquina del laboratorio.
# No se puede crear una "Máquina" directamente, solo se pueden crear PCs o Impresoras que usen este molde.
class Maquina(ABC):
    def __init__(self, codigo_equipo, tipo_equipo, estado_actual, area, fecha):
        self.codigo_equipo = codigo_equipo # ID único (ej: PC001)
        self.tipo_equipo = tipo_equipo     # Qué es (PC o IMP)
        self.estado_actual = estado_actual # Si sirve o está dañada
        self.area = area                   # Dónde está ubicada
        self.fecha = fecha                 # Cuándo se registró

    # Prueba
    """
    def mostrar_detalle(self):
        return f"Equipo: {self.codigo_equipo} | Tipo: {self.tipo_equipo} | Ubicado en: {self.area}"
    """