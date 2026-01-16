from app.models.Computadora import Computadora
from app.models.Impresora import Impresora
from app.models.Mantenimiento import Mantenimiento
from app.dtos.informe_dto import InformeMaquinaDTO

class ProyectoService:
    def __init__(self, maquina_dao, mantenimiento_dao):
        self._dao_maq = maquina_dao
        self._dao_mtto = mantenimiento_dao

    def registrar_maquina(self, datos_dict):
        tipo = datos_dict.get("tipo_equipo", "").upper()
        nueva = Computadora(datos_dict.get("codigo_equipo"), datos_dict.get("estado_actual"), 
                           datos_dict.get("area"), datos_dict.get("fecha")) if tipo == "PC" \
                else Impresora(datos_dict.get("codigo_equipo"), datos_dict.get("estado_actual"), 
                             datos_dict.get("area"), datos_dict.get("fecha"))
        self._dao_maq.guardar(nueva)
        return nueva, None

    def registrar_mantenimiento(self, datos_dict):
        codigo = datos_dict.get("codigo_maquina")
        maquina_db = self._dao_maq.buscar_por_codigo(codigo)
        if not maquina_db: return None, f"La máquina {codigo} no existe."

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

    # ESTA ES LA FUNCIÓN QUE BUSCA TU RUTA DE HISTORIAL
    def obtener_historial_por_maquina(self, codigo: str):
        registros = self._dao_mtto.listar_por_maquina(codigo)
        return registros

    # ESTA ES PARA EL REPORTE GENERAL (VENTANA 3)
    def obtener_informe_completo(self, codigo=None):
        if codigo:
            res = self._dao_maq.buscar_por_codigo(codigo)
            maquinas_db = [res] if res else []
            if not maquinas_db: return None, "Máquina no encontrada"
        else:
            maquinas_db = self._dao_maq.listar_todas()

        lista_informes = []
        for maq in maquinas_db:
            res_mongo = self._dao_mtto.listar_por_maquina(maq["codigo"])
            mttos_limpios = []
            for m in res_mongo:
                m["_id"] = str(m["_id"])
                mttos_limpios.append(m)

            informe = InformeMaquinaDTO(
                codigo=maq["codigo"],
                tipo=maq["tipo"],
                area=maq["area"],
                estado=maq["estado"],
                mantenimientos=mttos_limpios,
                total_mantenimientos=len(mttos_limpios)
            )
            lista_informes.append(informe)
        
        return lista_informes, None