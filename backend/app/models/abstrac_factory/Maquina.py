from abc import ABC

# Clase base para todas las máquinas del laboratorio
class Maquina(ABC):
    def __init__(self, codigo_equipo, tipo_equipo, estado_actual, area, fecha, usuario=None):
        self.codigo_equipo = codigo_equipo
        self.tipo_equipo = tipo_equipo
        self.estado_actual = estado_actual
        self.area = area
        self.fecha = fecha
        self.usuario = usuario  # Usuario asociado a la máquina