from pydantic import BaseModel
from typing import List

# DTO (Data Transfer Object) para empaquetar información de reportes
# Facilita comunicación con frontend
class InformeMaquinaDTO(BaseModel):
    codigo: str              # Código del equipo
    tipo: str                # Tipo de equipo
    area: str                # Ubicación
    estado: str              # Estado actual
    mantenimientos: List[dict] # Lista de mantenimientos desde MongoDB