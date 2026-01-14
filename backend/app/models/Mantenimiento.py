class Mantenimiento:
    # Metodo constructor
    def __init__(self, empresa, tecnico, tipo, fecha, observaciones):
        # Atributos privados
        self._empresa = empresa
        self._tecnico = tecnico
        self._tipo = tipo # Preventivo, Correctivo, etc.
        self._fecha = fecha
        self._observaciones = observaciones

    #Getters
    @property
    def empresa(self):
        return self._empresa
    @property
    def tecnico(self):
        return self._tecnico
    @property
    def tipo(self):
        return self._tipo
    @property
    def fecha(self):
        return self._fecha
    @property
    def observaciones(self):
        return self._observaciones
    
    #Setters
    @empresa.setter
    def empresa(self, valor):
        self._empresa = valor
    @tecnico.setter
    def tecnico(self, valor):
        self._tecnico = valor
    @tipo.setter
    def tipo(self, valor):
        self._tipo = valor
    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor
    @observaciones.setter
    def observaciones(self, valor):
        self._observaciones = valor