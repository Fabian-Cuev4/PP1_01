from app.models.abstrac_factory.Maquina import Maquina
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora

class MaquinaFactory:
    @staticmethod
    def crear_maquina(tipo: str, codigo: str, estado: str, area: str, fecha: str, usuario=None) -> Maquina:
        """
        Factory method para crear máquinas según su tipo
        """
        tipo_normalizado = tipo.upper().strip()
        
        if tipo_normalizado in ['PC', 'COMPUTADORA', 'COMPUTADOR']:
            return Computadora(codigo, tipo_normalizado, estado, area, fecha, usuario)
        elif tipo_normalizado in ['IMP', 'IMPRESORA']:
            return Impresora(codigo, tipo_normalizado, estado, area, fecha, usuario)
        else:
            raise ValueError(f"Tipo de máquina no válido: {tipo}. Debe ser PC/COMPUTADORA o IMP/IMPRESORA")
