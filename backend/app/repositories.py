from app.models import Maquina, Mantenimiento

class ProyectoRepository:
    def __init__(self):
        # Listas en memoria para simular una base de datos
        self._maquinas = []
        self._mantenimientos = []

    #Métodos para Máquinas
    def guardar_maquina(self, maquina: Maquina):
        self._maquinas.append(maquina)
        return maquina

    def obtener_todas_maquinas(self):
        return self._maquinas

    def buscar_maquina_por_codigo(self, codigo: str):
        # Buscamos el objeto Maquina que coincida con el código
        for m in self._maquinas:
            if m.codigo_equipo == codigo:
                return m
        return None

    #Métodos para Mantenimientos
    def guardar_mantenimiento(self, mantenimiento: Mantenimiento):
        self._mantenimientos.append(mantenimiento)
        return mantenimiento

    def obtener_mantenimientos_por_maquina(self, codigo_maquina: str):
        # Filtramos los mantenimientos que pertenecen a esa máquina específica
        return [mtto for mtto in self._mantenimientos if mtto.codigo_maquina_vinculada == codigo_maquina]
repo_instancia = ProyectoRepository()