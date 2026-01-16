from app.models.abstrac_factory.Maquina import Maquina

# Representa una computadora física dentro del laboratorio
class Computadora(Maquina):
    def __init__(self, codigo_equipo, estado_actual, area, fecha):
        # Hereda (copia) la estructura básica de una 'Máquina'
        super().__init__(codigo_equipo, "Computadora", estado_actual, area, fecha)

    # Prueba
    # Puede tener comportamientos específicos de una PC si se deseara
    def encender(self):
        return f"La computadora {self.codigo_equipo} está encendiendo..."