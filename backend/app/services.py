from app.models.Computadora import Computadora
from app.models.Impresora import Impresora
from app.models.Mantenimiento import Mantenimiento
from app.dtos.informe_dto import InformeMaquinaDTO

# Esta clase es como el "jefe de cocina" de la aplicación.
# Recibe las órdenes de las rutas y decide qué ingredientes (modelos) usar y cómo guardarlos.
class ProyectoService:
    def __init__(self, maquina_dao, mantenimiento_dao):
        # Guardamos las herramientas para guardar datos (DAOs)
        self._dao_maq = maquina_dao
        self._dao_mtto = mantenimiento_dao

    # Esta función se encarga de crear una máquina nueva (PC o Impresora)
    def registrar_maquina(self, datos_dict):
        codigo = datos_dict.get("codigo_equipo")
        
        # Primero revisamos que no exista otra máquina con el mismo código
        maquina_existente = self._dao_maq.buscar_por_codigo(codigo)
        if maquina_existente:
            return None, f"El código '{codigo}' ya existe. El código debe ser único."
        
        tipo = datos_dict.get("tipo_equipo", "").upper()
        # Según el tipo que eligió el usuario, creamos el objeto correcto
        if tipo == "PC":
            nueva = Computadora(
                datos_dict.get("codigo_equipo"), 
                datos_dict.get("estado_actual"), 
                datos_dict.get("area"), 
                datos_dict.get("fecha")
            )
        elif tipo == "IMP":
            nueva = Impresora(
                datos_dict.get("codigo_equipo"), 
                datos_dict.get("estado_actual"), 
                datos_dict.get("area"), 
                datos_dict.get("fecha")
            )
        else:
            return None, f"Tipo de equipo '{tipo}' no válido."
        
        # Le pedimos al DAO que guarde la máquina física en la base de datos MySQL
        try:
            self._dao_maq.guardar(nueva)
            return nueva, None
        except Exception as e:
            return None, f"Error al guardar la máquina: {str(e)}"

    # Esta función se encarga de anotar un mantenimiento para una máquina
    def registrar_mantenimiento(self, datos_dict):
        codigo = datos_dict.get("codigo_maquina")
        # Primero buscamos si la máquina existe en nuestra base de datos
        maquina_db = self._dao_maq.buscar_por_codigo(codigo)
        if not maquina_db: 
            return None, f"La máquina {codigo} no existe."

        # Identificamos qué tipo de máquina es para reconstruir el objeto
        tipo_maquina = maquina_db.get('tipo', '').upper()
        if tipo_maquina in ['COMPUTADORA', 'PC']:
            maquina_obj = Computadora(
                maquina_db['codigo'], maquina_db['estado'], maquina_db['area'], maquina_db['fecha']
            )
        elif tipo_maquina in ['IMPRESORA', 'IMP']:
            maquina_obj = Impresora(
                maquina_db['codigo'], maquina_db['estado'], maquina_db['area'], maquina_db['fecha']
            )
        else:
            return None, f"Tipo de máquina no reconocido."

        # Creamos el registro de mantenimiento vinculado a esa máquina
        nuevo_mtto = Mantenimiento(
            maquina_objeto=maquina_obj,
            empresa=datos_dict.get("empresa"),
            tecnico=datos_dict.get("tecnico"),
            tipo=datos_dict.get("tipo"),
            fecha=datos_dict.get("fecha"),
            observaciones=datos_dict.get("observaciones")
        )
        # Guardamos el mantenimiento en MongoDB (porque es una lista que crece mucho)
        self._dao_mtto.guardar(nuevo_mtto)
        return nuevo_mtto, None

    # Trae todos los mantenimientos de una máquina específica
    def obtener_historial_por_maquina(self, codigo: str):
        return self._dao_mtto.listar_por_maquina(codigo)

    # Crea el reporte resumido de máquinas con sus respectivos mantenimientos
    def obtener_informe_completo(self, codigo=None):
        """
        Genera el reporte cruzando datos de MySQL y MongoDB.
        Unificamos la lógica para que 'Ver Todo' y 'Buscar' usen siempre la misma fuente de datos.
        """
        # Obtenemos TODAS las máquinas (Fuente única de verdad)
        todas_las_maquinas = self._dao_maq.listar_todas()
        
        # Filtramos en memoria si el usuario envió un código
        if codigo:
            filtro = str(codigo).strip().lower()
            maquinas_db = [
                m for m in todas_las_maquinas 
                if filtro in str(m.get("codigo", "")).lower()
            ]
        else:
            maquinas_db = todas_las_maquinas

        if not maquinas_db:
            return [], None

        # Obtenemos TODOS los mantenimientos registrados en MongoDB
        todos_mttos = self._dao_mtto.listar_todos() or []
        
        # Creamos un mapa de mantenimientos agrupados por código normalizado
        mttos_map = {}
        for mt in todos_mttos:
            # Buscamos el código en campos comunes para mayor seguridad
            raw_c = mt.get("codigo_maquina") or mt.get("codigo")
            if raw_c:
                key = str(raw_c).strip().lower()
                if key not in mttos_map:
                    mttos_map[key] = []
                
                # Preparamos el registro para el JSON
                mt["_id"] = str(mt["_id"])
                # Aseguramos campo 'tipo' por compatibilidad
                if "tipo" not in mt:
                    mt["tipo"] = mt.get("_tipo", "N/A")
                
                mttos_map[key].append(mt)

        # Cruzamos los datos para armar el reporte final
        resultado_reporte = []
        for maq in maquinas_db:
            # Usamos el código oficial de la máquina para buscar en el mapa
            k_maq = str(maq.get("codigo", "")).strip().lower()
            mttos_encontrados = mttos_map.get(k_maq, [])
            
            # Empaquetamos en el DTO oficial
            resultado_reporte.append(InformeMaquinaDTO(
                codigo=maq["codigo"],
                tipo=maq["tipo"],
                area=maq["area"],
                estado=maq["estado"],
                mantenimientos=mttos_encontrados
            ))
        
        return resultado_reporte, None