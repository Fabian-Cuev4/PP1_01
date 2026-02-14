# Representa un mantenimiento realizado a una máquina
class Mantenimiento:
    def __init__(self, maquina_objeto, empresa, tecnico, tipo, fecha, observaciones, usuario=None):
        self.maquina = maquina_objeto
        self.empresa = empresa
        self.tecnico = tecnico
        self.tipo = tipo
        self.fecha = fecha
        self.observaciones = observaciones
        self.usuario = usuario  # Usuario asociado al mantenimiento

    @property
    def codigo_maquina_vinculada(self):
        return self.maquina.codigo_equipo

    def to_dict(self):
        return {
            "codigo_maquina": self.maquina.get("codigo", "") if isinstance(self.maquina, dict) else self.maquina.codigo_equipo,
            "empresa": self.empresa,
            "tecnico": self.tecnico,
            "tipo": self.tipo,
            "fecha": self.fecha,
            "observaciones": self.observaciones,
            "usuario": self.usuario
        }