from app.models.abstrac_factory.Maquina import Maquina

# Representa una impresora física dentro del laboratorio
class Impresora(Maquina):
    def __init__(self, codigo_equipo, estado_actual, area, fecha):
        # Hereda (copia) la estructura básica de una 'Máquina'
        super().__init__(codigo_equipo, "Impresora", estado_actual, area, fecha)

    # Prueba
    """
    def imprimir_prueba(self):
        return f"La impresora {self.codigo_equipo} está imprimiendo una página de prueba."
    """