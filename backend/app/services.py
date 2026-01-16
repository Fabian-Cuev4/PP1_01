from app.models.Computadora import Computadora
from app.models.Impresora import Impresora
from app.models.Mantenimiento import Mantenimiento

class ProyectoService:
    def __init__(self, maquina_dao, mantenimiento_dao):
        self._dao_maq = maquina_dao    # MySQL
        self._dao_mtto = mantenimiento_dao  # MongoDB

    def registrar_maquina(self, datos_dict):
        tipo = datos_dict.get("tipo_equipo", "").upper()
        if tipo == "PC":
            nueva = Computadora(datos_dict.get("codigo_equipo"), datos_dict.get("estado_actual"), 
                               datos_dict.get("area"), datos_dict.get("fecha"))
        else:
            nueva = Impresora(datos_dict.get("codigo_equipo"), datos_dict.get("estado_actual"), 
                             datos_dict.get("area"), datos_dict.get("fecha"))
        
        self._dao_maq.guardar(nueva)
        return nueva, None

    def registrar_mantenimiento(self, datos_dict):
        codigo = datos_dict.get("codigo_maquina")
        # Validamos que la máquina exista en MySQL
        maquina_db = self._dao_maq.buscar_por_codigo(codigo)

        if not maquina_db:
            return None, f"La máquina {codigo} no existe en MySQL."

        # Reconstruimos el objeto para el modelo de Mantenimiento
        maquina_obj = Computadora(maquina_db['codigo'], maquina_db['estado'], 
                                 maquina_db['area'], maquina_db['fecha'])

        nuevo_mtto = Mantenimiento(
            maquina_objeto=maquina_obj,
            empresa=datos_dict.get("empresa"),
            tecnico=datos_dict.get("tecnico"),
            tipo=datos_dict.get("tipo"),
            fecha=datos_dict.get("fecha"),
            observaciones=datos_dict.get("observaciones")
        )
        
        self._dao_mtto.guardar(nuevo_mtto)
        return nuevo_mtto, None

    def obtener_historial_por_maquina(self, codigo_maquina):
        return self._dao_mtto.listar_por_maquina(codigo_maquina)