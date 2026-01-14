class Mantenimiento:
    # Metodo constructor
    def __init__(self, maquina_objeto, empresa, tecnico, tipo, fecha, observaciones):
        # Atributos privados
        self._maquina = maquina_objeto # Relación con Maquina
        self._empresa = empresa
        self._tecnico = tecnico
        self._tipo = tipo # Preventivo, Correctivo, etc.
        self._fecha = fecha
        self._observaciones = observaciones

    # Getter para sacar el código directamente de la máquina vinculada
    @property
    def codigo_maquina_vinculada(self):
        # Accedemos al getter de la clase Maquina
        return self._maquina.codigo_equipo

    @property
    def empresa(self):
        return self._empresa

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