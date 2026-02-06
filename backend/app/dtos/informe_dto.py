from pydantic import BaseModel
from typing import List

# El DTO (Data Transfer Object) sirve para empaquetar la información de una forma
# que el frontend pueda entender fácilmente cuando pide un reporte.
class InformeMaquinaDTO(BaseModel):
    codigo: str              # Código del equipo
    tipo: str                # Tipo de equipo
    area: str                # Ubicación
    estado: str              # Estado actual
    mantenimientos: List[dict] # Lista de todos los mantenimientos traídos de MongoDB