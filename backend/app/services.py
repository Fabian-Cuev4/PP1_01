from app.models.Computadora import Computadora
from app.models.Impresora import Impresora
from app.models.Mantenimiento import Mantenimiento

class ProyectoService:
    def __init__(self, repository, mantenimiento_dao):
        self._repo = repository        # Repositorio en RAM (Arreglo)
        self._dao_mtto = mantenimiento_dao  # DAO de MongoDB

    # --- LÓGICA DE MÁQUINAS (EN RAM) ---
    def registrar_maquina(self, datos_dict):
        tipo = datos_dict.get("tipo_equipo", "").upper()
        if tipo == "PC":
            nueva = Computadora(datos_dict.get("codigo_equipo"), datos_dict.get("estado_actual"), 
                               datos_dict.get("area"), datos_dict.get("fecha"))
        elif tipo == "IMP":
            nueva = Impresora(datos_dict.get("codigo_equipo"), datos_dict.get("estado_actual"), 
                             datos_dict.get("area"), datos_dict.get("fecha"))
        else:
            return None, "Tipo de equipo no soportado"
        
        self._repo.guardar_maquina(nueva)
        return nueva, None

    # --- LÓGICA DE MANTENIMIENTO (EN MONGO) ---
    def registrar_mantenimiento(self, datos_dict):
        codigo = datos_dict.get("codigo_maquina")
        
        # 1. Intentamos buscar la máquina en RAM
        maquina_obj = self._repo.buscar_maquina_por_codigo(codigo)

        # 2. SI NO EXISTE EN RAM, creamos un objeto genérico rápido
        # para que el modelo Mantenimiento no explote
        if not maquina_obj:
            from app.models.Computadora import Computadora # Importamos una clase base
            maquina_obj = Computadora(
                codigo_equipo=codigo, 
                estado_actual="Desconocido", 
                area="General", 
                fecha="2024-01-01"
            )

        # 3. Creamos el objeto mantenimiento con la maquina (sea la real o la generica)
        nuevo_mtto = Mantenimiento(
            maquina_objeto=maquina_obj,
            empresa=datos_dict.get("empresa"),
            tecnico=datos_dict.get("tecnico"),
            tipo=datos_dict.get("tipo"),
            fecha=datos_dict.get("fecha"),
            observaciones=datos_dict.get("observaciones")
        )
        
        try:
            # 4. Guardamos en MongoDB
            self._dao_mtto.guardar(nuevo_mtto)
            return nuevo_mtto, None
        except Exception as e:
            return None, f"Error en MongoDB: {str(e)}"

    def obtener_historial_por_maquina(self, codigo_maquina):
        """Consulta el DAO para traer el historial de la base de datos"""
        return self._dao_mtto.listar_por_maquina(codigo_maquina)