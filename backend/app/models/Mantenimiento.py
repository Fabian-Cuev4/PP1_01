# Representa un evento de revisión técnica para una máquina
class Mantenimiento:
    def __init__(self, maquina_objeto, empresa, tecnico, tipo, fecha, observaciones):
        self.maquina = maquina_objeto # Objeto de la máquina a la que se le hace el trabajo
        self.empresa = empresa       # Empresa que realiza el trabajo
        self.tecnico = tecnico       # Nombre del técnico responsable
        self.tipo = tipo             # Si fue correctivo o preventivo
        self.fecha = fecha           # Fecha del trabajo
        self.observaciones = observaciones # Comentarios adicionales

    @property
    def codigo_maquina_vinculada(self):
        #Propiedad para acceder al código de la máquina vinculada
        return self.maquina.codigo_equipo

    # Convierte este objeto en un diccionario simple para poder guardarlo en MongoDB
    def to_dict(self):
        return {
            "codigo_maquina": self.maquina.codigo_equipo,
            "empresa": self.empresa,
            "tecnico": self.tecnico,
            "tipo": self.tipo,
            "fecha": self.fecha,
            "observaciones": self.observaciones
        }