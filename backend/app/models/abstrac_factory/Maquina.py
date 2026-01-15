# app/models/abstrac_factory/Maquina.py
from abc import ABC

class Maquina(ABC):
    def __init__(self, codigo_equipo, estado_actual, area, fecha, tipo_maquina):
        self._codigo_equipo = codigo_equipo
        self._estado_actual = estado_actual # Atributo privado
        self._area = area
        self._fecha = fecha
        self._tipo_maquina = tipo_maquina

    @property
    def codigo_equipo(self):
        return self._codigo_equipo

    @property
    def estado_actual(self): # <--- ESTO permite usar m.estado_actual
        return self._estado_actual

    @property
    def area(self):
        return self._area

    @property
    def fecha(self):
        return self._fecha

    @property
    def tipo_maquina(self):
        return self._tipo_maquina