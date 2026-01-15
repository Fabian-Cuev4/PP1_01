# app/models/Mantenimiento.py

class Mantenimiento:
    def __init__(self, maquina_objeto, empresa, tecnico, tipo, fecha, observaciones):
        # maquina_objeto recibirá el objeto PC o Impresora completo
        self.maquina_objeto = maquina_objeto 
        self.empresa = empresa
        self.tecnico = tecnico
        self.tipo = tipo
        self.fecha = fecha
        self.observaciones = observaciones

    @property
    def codigo_maquina_vinculada(self):
        # Accedemos al código a través del objeto que recibimos en el constructor
        # Esto evita tener que importar el repo aquí
        return self.maquina_objeto.codigo_equipo