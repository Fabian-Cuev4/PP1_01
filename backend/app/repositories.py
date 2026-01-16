from app.models.abstrac_factory.Maquina import Maquina
from app.models.Mantenimiento import Mantenimiento
from app.daos.maquina_dao import MaquinaDAO
from app.daos.mantenimiento_dao import MantenimientoDAO

class ProyectoRepository:

    def __init__(self):
        # Conexiones a las bases de datos reales
        self.maquina_dao = MaquinaDAO()
        self.mantenimiento_dao = MantenimientoDAO()

    # Metodos para maquinas
    def guardar_maquina(self, maquina: Maquina):
        """Guarda una máquina en MySQL"""
        try:
            self.maquina_dao.guardar(maquina)
            return maquina
        except Exception as e:
            print(f"Error al guardar máquina: {e}")
            return None

    def obtener_todas_maquinas(self):
        """Obtiene todas las máquinas desde MySQL"""
        try:
            # El DAO devuelve diccionarios, necesitamos convertirlos a objetos Maquina
            maquinas_data = self.maquina_dao.listar_todas()
            maquinas = []
            for data in maquinas_data:
                # Crear objetos Maquina desde los datos de la base de datos
                # Necesitamos determinar el tipo específico (Computadora o Impresora)
                if data['tipo'].lower() in ['pc', 'laptop', 'computadora']:
                    from app.models.Computadora import Computadora
                    maquina = Computadora(
                        codigo_equipo=data['codigo'],
                        estado_actual=data['estado'],
                        area=data['area'],
                        fecha=data['fecha']
                    )
                elif data['tipo'].lower() in ['impresora', 'printer']:
                    from app.models.Impresora import Impresora
                    maquina = Impresora(
                        codigo_equipo=data['codigo'],
                        estado_actual=data['estado'],
                        area=data['area'],
                        fecha=data['fecha']
                    )
                else:
                    # Tipo genérico usando la clase base
                    maquina = Maquina(
                        codigo_equipo=data['codigo'],
                        tipo_equipo=data['tipo'],
                        estado_actual=data['estado'],
                        area=data['area'],
                        fecha=data['fecha']
                    )
                maquinas.append(maquina)
            return maquinas
        except Exception as e:
            print(f"Error al obtener máquinas: {e}")
            return []

    def buscar_maquina_por_codigo(self, codigo: str):
        """Busca una máquina por código en MySQL"""
        try:
            data = self.maquina_dao.buscar_por_codigo(codigo)
            if not data:
                return None

            # Convertir el diccionario a objeto Maquina
            if data['tipo'].lower() in ['pc', 'laptop', 'computadora']:
                from app.models.Computadora import Computadora
                return Computadora(
                    codigo_equipo=data['codigo'],
                    estado_actual=data['estado'],
                    area=data['area'],
                    fecha=data['fecha']
                )
            elif data['tipo'].lower() in ['impresora', 'printer']:
                from app.models.Impresora import Impresora
                return Impresora(
                    codigo_equipo=data['codigo'],
                    estado_actual=data['estado'],
                    area=data['area'],
                    fecha=data['fecha']
                )
            else:
                return Maquina(
                    codigo_equipo=data['codigo'],
                    tipo_equipo=data['tipo'],
                    estado_actual=data['estado'],
                    area=data['area'],
                    fecha=data['fecha']
                )
        except Exception as e:
            print(f"Error al buscar máquina: {e}")
            return None

    # Metodos para mantenimientos
    def guardar_mantenimiento(self, mantenimiento: Mantenimiento):
        """Guarda un mantenimiento en MongoDB"""
        try:
            self.mantenimiento_dao.guardar(mantenimiento)
            return mantenimiento
        except Exception as e:
            print(f"Error al guardar mantenimiento: {e}")
            return None

    def obtener_mantenimientos_por_maquina(self, codigo_maquina: str):
        """Obtiene mantenimientos de una máquina desde MongoDB"""
        try:
            # El DAO devuelve documentos de MongoDB, necesitamos convertirlos a objetos Mantenimiento
            mantenimientos_data = self.mantenimiento_dao.listar_por_maquina(codigo_maquina)
            mantenimientos = []

            for data in mantenimientos_data:
                # Para crear un objeto Mantenimiento, necesitamos el objeto máquina
                # Buscamos la máquina por código
                maquina = self.buscar_maquina_por_codigo(data['codigo_maquina'])
                if maquina:
                    mantenimiento = Mantenimiento(
                        maquina_objeto=maquina,
                        empresa=data['empresa'],
                        tecnico=data['tecnico'],
                        tipo=data['tipo'],
                        fecha=data['fecha'],
                        observaciones=data['observaciones']
                    )
                    mantenimientos.append(mantenimiento)

            return mantenimientos
        except Exception as e:
            print(f"Error al obtener mantenimientos: {e}")
            return []

# La instancia se crea al final
repo_instancia = ProyectoRepository()