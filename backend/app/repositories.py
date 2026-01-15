# app/repositories.py
# Asegúrate de que estas rutas coincidan con tus carpetas reales
from app.models.abstrac_factory.Maquina import Maquina 
from app.models.Mantenimiento import Mantenimiento

class ProyectoRepository:
    def __init__(self):
        # Listas que actúan como base de datos temporal
        self._maquinas = []
        self._mantenimientos = []

    # --- MÉTODOS PARA MÁQUINAS ---
    def guardar_maquina(self, maquina: Maquina):
        self._maquinas.append(maquina)
        return maquina

    def obtener_todas_maquinas(self):
        return self._maquinas

    def buscar_maquina_por_codigo(self, codigo: str):
        for m in self._maquinas:
            if m.codigo_equipo == codigo:
                return m
        return None

    # --- MÉTODOS PARA MANTENIMIENTOS ---
    def guardar_mantenimiento(self, mantenimiento: Mantenimiento):
        self._mantenimientos.append(mantenimiento)
        return mantenimiento

    def obtener_mantenimientos_por_maquina(self, codigo_maquina: str):
        # Aquí m.codigo_maquina_vinculada llama a la @property del modelo
        return [m for m in self._mantenimientos if m.codigo_maquina_vinculada == codigo_maquina]

# ESTO ES LO MÁS IMPORTANTE: La instancia se crea al final
repo_instancia = ProyectoRepository()