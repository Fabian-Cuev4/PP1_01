from app.repositories import ProyectoRepository
from app.models.Mantenimiento import Mantenimiento

class ProyectoService:
    def __init__(self, repository: ProyectoRepository):
        self._repo = repository

    def registrar_mantenimiento(self, datos_dict):
        #Extrae el código de la máquina para buscarla
        codigo_maq = datos_dict.get("codigo_maquina")
        maquina = self._repo.buscar_maquina_por_codigo(codigo_maq)

        if not maquina:
            return None, "La máquina no existe"

        #Crea el objeto usando el constructor de la clase Mantenimiento
        nuevo_mtto = Mantenimiento(
            maquina_objeto=maquina,
            empresa=datos_dict.get("empresa"),
            tecnico=datos_dict.get("tecnico"),
            tipo=datos_dict.get("tipo"),
            fecha=datos_dict.get("fecha"),
            observaciones=datos_dict.get("observaciones")
        )
        # Guarda objeto en el repo
        self._repo.guardar_mantenimiento(nuevo_mtto)
        return nuevo_mtto, None

    def obtener_historial_mantenimiento(self, codigo_maquina: str):
        # Primero verificamos si la máquina existe
        maquina = self._repo.buscar_maquina_por_codigo(codigo_maquina)
        if not maquina:
            return None, "No se encontró la máquina para ver el historial"
        
        # Obtenemos los mantenimientos desde el repo
        historial = self._repo.obtener_mantenimientos_por_maquina(codigo_maquina)
        return historial, None
        