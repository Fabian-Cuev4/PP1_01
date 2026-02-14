# Este archivo contiene la lógica principal del negocio
# Aquí se procesan los datos antes de guardarlos en la base de datos

# Importamos las clases que necesitamos
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora
from app.models.Mantenimiento import Mantenimiento
from app.models.abstrac_factory.MaquinaFactory import MaquinaFactory
from app.dtos.informe_dto import InformeMaquinaDTO

# Esta clase coordina todas las operaciones del sistema
class ProyectoService:
    # El constructor recibe los objetos que acceden a las bases de datos
    def __init__(self, maquina_dao, mantenimiento_dao):
        # Guardamos las referencias para usarlas después
        self._dao_maq = maquina_dao  # Objeto para acceder a la tabla de máquinas
        self._dao_mtto = mantenimiento_dao  # Objeto para acceder a la tabla de mantenimientos

    def registrar_maquina(self, datos_dict):
        # Esta función registra una nueva máquina en el sistema
        # Recibe un diccionario con los datos de la máquina
        
        # Primero obtenemos el código de la máquina
        codigo = datos_dict.get("codigo_equipo")
        
        # Verificamos que no exista otra máquina con el mismo código
        # Si ya existe, retornamos un error
        if self._dao_maq.buscar_por_codigo(codigo):
            return None, f"El código '{codigo}' ya existe."
        
        # Obtenemos el tipo de máquina (PC o IMP) y lo convertimos a mayúsculas
        tipo = datos_dict.get("tipo_equipo", "").upper()
        # Obtenemos el usuario que está registrando la máquina
        usuario = datos_dict.get("usuario")
        
        # Usamos el Factory Pattern para crear la máquina
        try:
            nueva = MaquinaFactory.crear_maquina(
                tipo, 
                datos_dict.get("codigo_equipo"), 
                datos_dict.get("estado_actual"), 
                datos_dict.get("area"), 
                datos_dict.get("fecha"),
                usuario
            )
        except ValueError as e:
            return None, str(e)
        
        # Intentamos guardar la máquina en la base de datos
        try:
            self._dao_maq.guardar(nueva)
            # Si todo salió bien, retornamos la máquina creada
            return nueva, None
        except Exception as e:
            # Si hubo un error, retornamos el mensaje de error
            return None, f"Error al guardar: {str(e)}"

    def actualizar_maquina(self, datos_dict):
        # Esta función actualiza los datos de una máquina existente
        # Recibe un diccionario con los nuevos datos
        
        # Obtenemos el código de la máquina a actualizar
        codigo = datos_dict.get("codigo_equipo")
        
        # Validamos que se proporcionó un código
        if not codigo:
            return None, "El código de la máquina es obligatorio."
        
        # Buscamos la máquina en la base de datos para verificar que existe
        maquina_db = self._dao_maq.buscar_por_codigo(codigo)
        
        # Si no encontramos la máquina, retornamos un error
        if not maquina_db:
            return None, f"La máquina {codigo} no existe."
        
        # Obtenemos los datos nuevos, si no vienen usamos los antiguos
        tipo = datos_dict.get("tipo_equipo", "").upper() or maquina_db.get('tipo', '').upper()
        estado = datos_dict.get("estado_actual") or maquina_db.get('estado')
        area = datos_dict.get("area") or maquina_db.get('area')
        fecha = datos_dict.get("fecha") or maquina_db.get('fecha')
        usuario = datos_dict.get("usuario") or maquina_db.get('usuario')
        
        # Usamos el Factory Pattern para crear el objeto máquina
        try:
            maquina_obj = MaquinaFactory.crear_maquina(
                tipo, codigo, estado, area, fecha, usuario
            )
        except ValueError as e:
            return None, str(e)
        
        # Intentamos actualizar en la base de datos
        if self._dao_maq.actualizar(maquina_obj):
            return maquina_obj, None
        return None, "Error al actualizar la máquina."

    def eliminar_maquina(self, codigo):
        # Esta función elimina una máquina y todos sus mantenimientos
        # Primero verificamos que la máquina exista
        if not self._dao_maq.buscar_por_codigo(codigo):
            return False, "La máquina no existe."
        
        # Eliminamos primero todos los mantenimientos de esa máquina
        self._dao_mtto.eliminar_por_maquina(codigo)
        
        # Luego eliminamos la máquina
        if self._dao_maq.eliminar(codigo):
            return True, None
        return False, "Error al eliminar la máquina."

    def registrar_mantenimiento(self, datos_dict):
        # Esta función registra un nuevo mantenimiento para una máquina
        # Obtenemos el código de la máquina
        codigo = datos_dict.get("codigo_maquina")
        # Buscamos la máquina en la base de datos
        maquina_db = self._dao_maq.buscar_por_codigo(codigo)
        
        # Si no existe la máquina, retornamos un error
        if not maquina_db:
            return None, f"La máquina {codigo} no existe."

        # Obtenemos el tipo de máquina para crear el objeto correcto
        tipo_maquina = maquina_db.get('tipo', '').upper()
        
        # Creamos el objeto máquina según su tipo
        if tipo_maquina in ['COMPUTADORA', 'PC']:
            maquina_obj = Computadora(
                maquina_db['codigo'],
                maquina_db['estado'],
                maquina_db['area'],
                maquina_db['fecha'],
                maquina_db.get('usuario')
            )
        elif tipo_maquina in ['IMPRESORA', 'IMP']:
            maquina_obj = Impresora(
                maquina_db['codigo'],
                maquina_db['estado'],
                maquina_db['area'],
                maquina_db['fecha'],
                maquina_db.get('usuario')
            )
        else:
            return None, "Tipo de máquina no reconocido."

        # Usamos el usuario del mantenimiento o el de la máquina
        usuario = datos_dict.get("usuario") or maquina_db.get('usuario')
        
        # Creamos el objeto mantenimiento con todos los datos
        nuevo_mtto = Mantenimiento(
            maquina_objeto=maquina_obj,
            empresa=datos_dict.get("empresa"),
            tecnico=datos_dict.get("tecnico"),
            tipo=datos_dict.get("tipo"),
            fecha=datos_dict.get("fecha"),
            observaciones=datos_dict.get("observaciones"),
            usuario=usuario
        )
        
        # Guardamos el mantenimiento en la base de datos
        self._dao_mtto.guardar(nuevo_mtto)
        return nuevo_mtto, None

    def obtener_historial_por_maquina(self, codigo):
        # Esta función obtiene todos los mantenimientos de una máquina
        # Simplemente le pedimos al DAO que busque los mantenimientos
        return self._dao_mtto.listar_por_maquina(codigo)

    def obtener_informe_completo(self, codigo=None):
        # Esta función genera un reporte completo de máquinas y mantenimientos
        # Primero obtenemos todas las máquinas
        todas_las_maquinas = self._dao_maq.listar_todas()
        
        # Si nos dieron un código, filtramos solo esa máquina
        if codigo:
            codigo_buscar = str(codigo).strip().lower()
            maquinas_db = []
            # Recorremos todas las máquinas
            for m in todas_las_maquinas:
                codigo_maq = str(m.get("codigo", "")).lower()
                # Si el código coincide, la agregamos a la lista
                if codigo_buscar in codigo_maq:
                    maquinas_db.append(m)
        else:
            # Si no nos dieron código, usamos todas las máquinas
            maquinas_db = todas_las_maquinas

        # Si no hay máquinas, retornamos una lista vacía
        if not maquinas_db:
            return [], None

        # Obtenemos todos los mantenimientos de todas las máquinas
        todos_mttos = self._dao_mtto.listar_todos() or []
        
        # Agrupamos los mantenimientos por código de máquina
        # Usamos un diccionario donde la clave es el código de la máquina
        mttos_por_maquina = {}
        for mt in todos_mttos:
            # Obtenemos el código de la máquina del mantenimiento
            codigo_mt = mt.get("codigo_maquina") or mt.get("codigo")
            if codigo_mt:
                # Normalizamos el código (minúsculas y sin espacios)
                codigo_key = str(codigo_mt).strip().lower()
                # Si no existe esa clave, creamos una lista vacía
                if codigo_key not in mttos_por_maquina:
                    mttos_por_maquina[codigo_key] = []
                # Convertimos el ID de MongoDB a string (para que se pueda enviar como JSON)
                if "_id" in mt:
                    mt["_id"] = str(mt["_id"])
                # Si no tiene tipo, le ponemos "N/A"
                if "tipo" not in mt:
                    mt["tipo"] = "N/A"
                # Agregamos el mantenimiento a la lista de esa máquina
                mttos_por_maquina[codigo_key].append(mt)

        # Construimos el reporte final
        resultado = []
        for maq in maquinas_db:
            # Obtenemos el código de la máquina normalizado
            codigo_maq = str(maq.get("codigo", "")).strip().lower()
            # Obtenemos los mantenimientos de esa máquina (si tiene)
            mttos = mttos_por_maquina.get(codigo_maq, [])
            
            # Creamos un objeto DTO con la información de la máquina y sus mantenimientos
            resultado.append(InformeMaquinaDTO(
                codigo=maq["codigo"],
                tipo=maq["tipo"],
                area=maq["area"],
                estado=maq["estado"],
                mantenimientos=mttos
            ))
        
        # Retornamos el resultado
        return resultado, None
    
    def listar_todas_maquinas(self):
        # Obtiene todas las máquinas del sistema
        
        # Returns:
        #     list: Lista de todas las máquinas
        try:
            return self._dao_maq.listar_todas()
        except Exception as e:
            raise Exception(f"Error al listar máquinas: {str(e)}")
