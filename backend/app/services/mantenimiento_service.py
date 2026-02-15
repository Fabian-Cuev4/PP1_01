# SERVICE - Toda la lógica de negocio de mantenimientos
# Responsabilidades: validación, transformación, normalización, lógica de negocio

from app.daos.mantenimiento_dao import MantenimientoDAO
from app.daos.maquina_dao import MaquinaDAO
from app.models.Mantenimiento import Mantenimiento
from app.dtos.informe_dto import InformeMaquinaDTO

class MantenimientoService:
    def __init__(self):
        self.dao = MantenimientoDAO()
        self.maquina_dao = MaquinaDAO()

    # Registra nuevo mantenimiento con validación completa
    def registrar_mantenimiento(self, datos: dict) -> tuple:
        # Validación de datos obligatorios
        if not all([datos.get("codigo_maquina"), datos.get("empresa"), 
                   datos.get("tecnico"), datos.get("tipo"), 
                   datos.get("fecha"), datos.get("observaciones")]):
            return None, "Todos los campos son obligatorios"

        codigo_maquina = datos["codigo_maquina"].strip()
        
        # Verificar que la máquina existe (case-insensitive)
        maquina_service = __import__('app.services.maquina_service', fromlist=['MaquinaService']).MaquinaService()
        maquina = maquina_service.obtener_por_codigo(codigo_maquina)
        if not maquina:
            return None, f"La máquina '{codigo_maquina}' no existe"

        # Normalización del tipo de mantenimiento
        tipo = datos["tipo"].strip().lower()
        if tipo not in ["preventivo", "correctivo"]:
            return None, "El tipo debe ser 'preventivo' o 'correctivo'"

        # Creación del objeto mantenimiento
        try:
            mantenimiento = Mantenimiento(
                maquina_objeto=maquina,
                empresa=datos["empresa"].strip(),
                tecnico=datos["tecnico"].strip(),
                tipo=tipo,
                fecha=datos["fecha"].strip(),
                observaciones=datos["observaciones"].strip(),
                usuario=datos.get("usuario", "").strip()
            )

            # Guardado en base de datos
            if self.dao.insertar(
                codigo_maquina,
                datos["empresa"].strip(),
                datos["tecnico"].strip(),
                tipo,
                datos["fecha"].strip(),
                datos["observaciones"].strip(),
                datos.get("usuario", "").strip()
            ):
                return {"mensaje": "Mantenimiento registrado", "codigo_maquina": codigo_maquina}, None
            else:
                return None, "Error al guardar en base de datos"
                
        except ValueError as e:
            return None, str(e)

    # Obtiene historial de mantenimientos de una máquina (ordenado por fecha)
    def obtener_historial(self, codigo_maquina: str) -> tuple:
        codigo_normalizado = codigo_maquina.strip()
        
        # Verificar que la máquina existe
        maquina_service = __import__('app.services.maquina_service', fromlist=['MaquinaService']).MaquinaService()
        maquina = maquina_service.obtener_por_codigo(codigo_normalizado)
        if not maquina:
            return None, f"La máquina '{codigo_normalizado}' no existe"

        # Obtener mantenimientos ordenados por fecha (más reciente primero)
        mantenimientos = self.dao.listar_por_maquina_ordenados(codigo_normalizado, -1)
        
        # Transformación de datos para el frontend
        resultado = []
        for mant in mantenimientos:
            # Convertir ObjectId a string
            if "_id" in mant:
                mant["_id"] = str(mant["_id"])
            
            # Asegurar que tenga todos los campos esperados
            if "tipo" not in mant:
                mant["tipo"] = "N/A"
            
            resultado.append(mant)
        
        return resultado, None

    # Genera informe general delegando al DTO
    def generar_informe_general(self, codigo_filtro: str = None) -> tuple:
        # El service solo coordina, el DTO obtiene los datos de MySQL + MongoDB
        try:
            # El DTO mismo obtiene y combina los datos de ambas bases
            resultado = InformeMaquinaDTO.crear_reporte_general(codigo_filtro)
            return resultado, None
        except Exception as e:
            return None, f"Error al generar informe: {str(e)}"

    # Elimina mantenimientos de una máquina
    def eliminar_por_maquina(self, codigo_maquina: str) -> tuple:
        codigo_normalizado = codigo_maquina.strip()
        
        # Verificar que la máquina existe
        maquina_service = __import__('app.services.maquina_service', fromlist=['MaquinaService']).MaquinaService()
        maquina = maquina_service.obtener_por_codigo(codigo_normalizado)
        if not maquina:
            return 0, f"La máquina '{codigo_normalizado}' no existe"

        # Eliminar mantenimientos
        eliminados = self.dao.eliminar_por_maquina(codigo_normalizado)
        return eliminados, None
