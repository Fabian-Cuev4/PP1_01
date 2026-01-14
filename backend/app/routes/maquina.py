from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Maquina(BaseModel):
    codigo_equipo: str
    estado_equipo: str
    area_equipo: str
    fecha_adquision: str
maquinas: List[Maquina] = []

#Rutas de acciones 
@app.post("/maquinas", tags=["maquinas"])
def agregar_maquina(maquina: Maquina):
    maquinas.append(maquina)
    return {"ok": True}