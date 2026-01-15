from app.repositories import ProyectoRepository
from app.models.Mantenimiento import Mantenimiento
# Importamos las clases hijas y la base
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora

class ProyectoService:
    def __init__(self, repository: ProyectoRepository):
        self._repo = repository

    # --- NUEVO MÉTODO PARA REGISTRAR MÁQUINAS ---
    def registrar_maquina(self, datos_dict):
        tipo = datos_dict.get("tipo_equipo", "").upper()
        
        # IDENTIFICACIÓN: Aquí decidimos qué clase instanciar
        if tipo == "PC":
            nueva_maquina = Computadora(
                codigo_equipo=datos_dict.get("codigo_equipo"),
                estado_actual=datos_dict.get("estado_actual"),
                area=datos_dict.get("area"),
                fecha=datos_dict.get("fecha")
            )
        elif tipo == "IMP":
            nueva_maquina = Impresora(
                codigo_equipo=datos_dict.get("codigo_equipo"),
                estado_actual=datos_dict.get("estado_actual"),
                area=datos_dict.get("area"),
                fecha=datos_dict.get("fecha")
            )
        else:
            return None, "Tipo de equipo no reconocido"

        # Guardamos en el repo
        self._repo.guardar_maquina(nueva_maquina)
        return nueva_maquina, None

    # Tus otros métodos se quedan igual
    def registrar_mantenimiento(self, datos_dict):
        codigo_maq = datos_dict.get("codigo_maquina")
        maquina = self._repo.buscar_maquina_por_codigo(codigo_maq)

        if not maquina:
            return None, "La máquina no existe"

        nuevo_mtto = Mantenimiento(
            maquina_objeto=maquina,
            empresa=datos_dict.get("empresa"),
            tecnico=datos_dict.get("tecnico"),
            tipo=datos_dict.get("tipo"),
            fecha=datos_dict.get("fecha"),
            observaciones=datos_dict.get("observaciones")
        )
        self._repo.guardar_mantenimiento(nuevo_mtto)
        return nuevo_mtto, None

    def obtener_historial_mantenimiento(self, codigo_maquina: str):
        maquina = self._repo.buscar_maquina_por_codigo(codigo_maquina)
        if not maquina:
            return None, "No se encontró la máquina"
        
        historial = self._repo.obtener_mantenimientos_por_maquina(codigo_maquina)
        return historial, None