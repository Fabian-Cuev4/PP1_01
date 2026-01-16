from pydantic import BaseModel
from typing import List

class InformeMaquinaDTO(BaseModel):
    codigo: str
    tipo: str
    area: str
    estado: str
    mantenimientos: List[dict] = []
    total_mantenimientos: int = 0