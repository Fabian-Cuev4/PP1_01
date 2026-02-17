# SERVICE - Toda la lógica de negocio de máquinas
# Responsabilidades: validación, transformación, normalización, lógica de negocio

import json
from app.database.redis_client import redis_client
from app.daos.maquina_dao import MaquinaDAO
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora

class MaquinaService:
    def __init__(self):
        self.dao = MaquinaDAO()

    # Registra nueva máquina con validación completa
    def registrar_maquina(self, datos: dict) -> tuple:
        # Validación de datos obligatorios
        if not all([datos.get("codigo_equipo"), datos.get("tipo_equipo"), 
                   datos.get("estado_actual"), datos.get("area"), datos.get("fecha")]):
            return None, "Todos los campos son obligatorios"

        # Normalización del código
        codigo = datos["codigo_equipo"].strip()
        
        # Verificación de duplicados (case-insensitive)
        if self._existe_codigo(codigo):
            return None, f"El código '{codigo}' ya existe"

        # Normalización del tipo
        tipo = datos["tipo_equipo"].strip().upper()
        
        # Validación del tipo
        if tipo not in ["PC", "IMP"]:
            return None, "Tipo de equipo no válido (debe ser PC o IMP)"

        try:
            # Creación del objeto usando Factory Pattern
            if tipo == "PC":
                maquina = Computadora(codigo, datos["estado_actual"], 
                                    datos["area"], datos["fecha"], 
                                    datos.get("usuario"))
            else:  # IMP
                maquina = Impresora(codigo, datos["estado_actual"], 
                                   datos["area"], datos["fecha"], 
                                   datos.get("usuario"))

            # Guardado en base de datos
            if self.dao.insertar(
                maquina.codigo_equipo,
                maquina.tipo_equipo,
                maquina.estado_actual,
                maquina.area,
                maquina.fecha,
                maquina.usuario
            ):
                redis_client.delete("siglab:maquinas:listar")
                return {"mensaje": "Máquina registrada", "codigo": codigo}, None
            else:
                return None, "Error al guardar en base de datos"
                
        except ValueError as e:
            return None, str(e)

    # Actualiza máquina existente
    def actualizar_maquina(self, datos: dict) -> tuple:
        if not datos.get("codigo_equipo"):
            return None, "El código de la máquina es obligatorio"

        codigo = datos["codigo_equipo"].strip()
        
        # Verificar que existe
        maquina_existente = self.dao.buscar_por_codigo_exacto(codigo)
        if not maquina_existente:
            return None, "La máquina no existe"

        # Normalización del tipo
        tipo = datos.get("tipo_equipo", "").strip().upper() or maquina_existente.get("tipo", "").upper()
        
        # Validación del tipo
        if tipo not in ["PC", "IMP", "COMPUTADORA", "IMPRESORA"]:
            return None, "Tipo de máquina no reconocido"

        # Mapeo de tipos
        tipo_normalizado = "PC" if tipo in ["PC", "COMPUTADORA"] else "IMP"

        # Actualización
        if self.dao.actualizar(
            codigo,
            tipo_normalizado,
            datos.get("estado_actual") or maquina_existente.get("estado"),
            datos.get("area") or maquina_existente.get("area"),
            datos.get("fecha") or maquina_existente.get("fecha"),
            datos.get("usuario") or maquina_existente.get("usuario")
        ):
            redis_client.delete("siglab:maquinas:listar")
            return {"mensaje": "Máquina actualizada", "codigo": codigo}, None
        else:
            return None, "Error al actualizar la máquina"

    # Elimina máquina y sus mantenimientos
    def eliminar_maquina(self, codigo: str) -> tuple:
        codigo = codigo.strip()
        
        # Verificar que existe
        if not self.dao.buscar_por_codigo_exacto(codigo):
            return False, "La máquina no existe"

        # Eliminar (los mantenimientos se eliminan por cascade o en otro servicio)
        if self.dao.eliminar(codigo):
            redis_client.delete("siglab:maquinas:listar")
            return True, "Máquina eliminada correctamente"
        else:
            return False, "Error al eliminar la máquina"

    # Busca máquinas con lógica de búsqueda flexible
    def buscar_maquinas(self, termino: str = None) -> list:
        cache_key = "siglab:maquinas:listar"

        # SOLO cacheamos cuando es listado completo
        if not termino:
            # 1 Revisar cache
            maquinas_cache = redis_client.get(cache_key)

            if maquinas_cache:
                print("📦 Desde Redis")
                return json.loads(maquinas_cache)

            # 2️ Consultar base de datos
            maquinas = self.dao.listar_todas()
            
            # 3️ Convertir fechas a string para JSON
            for maquina in maquinas:
                if 'fecha' in maquina and hasattr(maquina['fecha'], 'strftime'):
                    maquina['fecha'] = maquina['fecha'].strftime('%Y-%m-%d')
            
            # 4️ Guardar en Redis con TTL (60 segundos)
            redis_client.setex(cache_key, 60, json.dumps(maquinas))
            print("💾 Guardado en Redis")

            return maquinas

        # Si hay término, NO usamos cache
        termino_normalizado = termino.strip().lower()
        todas = self.dao.listar_todas()

        # Convertir fechas para búsquedas con término
        for maquina in todas:
            if 'fecha' in maquina and hasattr(maquina['fecha'], 'strftime'):
                maquina['fecha'] = maquina['fecha'].strftime('%Y-%m-%d')

        filtradas = []
        for maquina in todas:
            codigo_maquina = str(maquina.get("codigo", "")).lower()
            if termino_normalizado in codigo_maquina:
                filtradas.append(maquina)

        return filtradas


    # Verifica si existe código (case-insensitive)
    def _existe_codigo(self, codigo: str) -> bool:
        codigo_normalizado = codigo.strip().lower()
        todas = self.dao.listar_todas()
        
        for maquina in todas:
            codigo_db = str(maquina.get("codigo", "")).lower()
            if codigo_normalizado == codigo_db:
                return True
        return False

    # Obtiene máquina por código (case-insensitive)
    def obtener_por_codigo(self, codigo: str) -> dict:
        codigo_normalizado = codigo.strip().lower()
        todas = self.dao.listar_todas()
        
        for maquina in todas:
            codigo_db = str(maquina.get("codigo", "")).lower()
            if codigo_normalizado == codigo_db:
                return maquina
        return None
