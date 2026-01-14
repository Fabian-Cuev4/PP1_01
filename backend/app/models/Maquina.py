class Maquina:
    #Metodo constructor
    def __init__(self, codigo_equipo, estado_actual, area, fecha):
        # Atributos privados
        self._codigo_equipo = codigo_equipo
        self._estado_actual = estado_actual  # Operativo, Mantenimiento, Fuera de Servicio
        self._area = area
        self._fecha = fecha

    #Getters
    @property
    def codigo_equipo(self):
        return self._codigo_equipo

    @property
    def estado_actual(self):
        return self._estado_actual

    @property
    def area(self):
        return self._area

    @property
    def fecha(self):
        return self._fecha

    #Setters
    @codigo_equipo.setter
    def codigo_equipo(self, valor):
        self._codigo_equipo = valor

    @estado_actual.setter
    def estado_actual(self, valor):
        # Aquí podrías agregar validación para asegurar que solo entren estados permitidos
        self._estado_actual = valor

    @area.setter
    def area(self, valor):
        self._area = valor

    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor
