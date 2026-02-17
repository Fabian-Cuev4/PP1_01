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

    # Registra nueva máquina con validación completa y resiliencia Redis
    def registrar_maquina(self, datos: dict) -> tuple:
        # Validación de datos obligatorios
        if not all([datos.get("codigo_equipo"), datos.get("tipo_equipo"), 
                   datos.get("estado_actual"), datos.get("area"), datos.get("fecha")]):
            return None, "Todos los campos son obligatorios"

        # Normalización del código
        codigo = datos["codigo_equipo"].strip()
        
        # Verificación de duplicados (case-insensitive) - con fallback Redis
        if self._existe_codigo_con_redis(codigo):
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

            # Preparar datos para Redis (consistentes con DB)
            datos_maquina = {
                "codigo": maquina.codigo_equipo,
                "tipo": maquina.tipo_equipo,
                "estado": maquina.estado_actual,
                "area": maquina.area,
                "fecha": maquina.fecha,
                "usuario": maquina.usuario or ""
            }

            # ESTRATEGIA WRITE-THROUGH con RESILIENCIA
            db_exitoso = False
            redis_exitoso = False
            
            # 1️⃣ Intentar guardar en Base de Datos
            try:
                db_exitoso = self.dao.insertar(
                    maquina.codigo_equipo,
                    maquina.tipo_equipo,
                    maquina.estado_actual,
                    maquina.area,
                    maquina.fecha,
                    maquina.usuario
                )
            except Exception as db_error:
                print(f"⚠️ Error DB: {str(db_error)}")
                db_exitoso = False

            # 2️⃣ Siempre intentar guardar en Redis (incluso si DB falla)
            try:
                # Guardar máquina individual en Redis
                redis_client.setex(
                    f"siglab:maquina:{codigo.lower()}",
                    3600,  # 1 hora TTL para máquinas individuales
                    json.dumps(datos_maquina)
                )
                
                # Actualizar lista completa en Redis
                self._actualizar_cache_redis_con_nueva_maquina(datos_maquina)
                redis_exitoso = True
                
            except Exception as redis_error:
                print(f"⚠️ Error Redis: {str(redis_error)}")
                redis_exitoso = False

            # 3️⃣ Lógica de resiliencia y respuesta
            if db_exitoso and redis_exitoso:
                # ✅ Éxito completo
                print("✅ Máquina guardada en DB y Redis")
                return {"mensaje": "Máquina registrada (DB + Redis)", "codigo": codigo}, None
                
            elif db_exitoso and not redis_exitoso:
                # ⚠️ Solo DB (Redis caído)
                print("⚠️ Máquina guardada solo en DB (Redis no disponible)")
                return {"mensaje": "Máquina registrada (solo DB)", "codigo": codigo}, None
                
            elif not db_exitoso and redis_exitoso:
                # 🔄 Solo Redis (DB caída) - Modo resiliencia
                print("🔄 Máquina guardada solo en Redis (DB no disponible)")
                return {"mensaje": "Máquina registrada (solo Redis - modo resiliencia)", "codigo": codigo}, None
                
            else:
                # ❌ Falla completa
                return None, "Error crítico: No se pudo guardar en DB ni Redis"
                
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

    # Busca máquinas con lógica de búsqueda flexible y resiliencia Redis
    def buscar_maquinas(self, termino: str = None) -> list:
        cache_key = "siglab:maquinas:listar"

        # SOLO cacheamos cuando es listado completo
        if not termino:
            # 1 Revisar cache
            maquinas_cache = redis_client.get(cache_key)

            if maquinas_cache:
                print("📦 Desde Redis")
                return json.loads(maquinas_cache)

            # 2️ Consultar base de datos con fallback a Redis
            try:
                maquinas = self.dao.listar_todas()
                print("🗄️ Desde MySQL")
            except Exception as db_error:
                print(f"⚠️ Error MySQL: {str(db_error)} - Intentando fallback Redis")
                maquinas = self._obtener_maquinas_desde_redis_fallback()
            
            # 3️ Convertir fechas a string para JSON
            for maquina in maquinas:
                if 'fecha' in maquina and hasattr(maquina['fecha'], 'strftime'):
                    maquina['fecha'] = maquina['fecha'].strftime('%Y-%m-%d')
            
            # 4️ Guardar en Redis con TTL (60 segundos)
            try:
                redis_client.setex(cache_key, 60, json.dumps(maquinas))
                print("💾 Guardado en Redis")
            except Exception as redis_error:
                print(f"⚠️ No se pudo guardar en Redis: {str(redis_error)}")

            return maquinas

        # Si hay término, NO usamos cache
        termino_normalizado = termino.strip().lower()
        
        try:
            todas = self.dao.listar_todas()
        except Exception:
            todas = self._obtener_maquinas_desde_redis_fallback()

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

    # Método auxiliar: Verificación de duplicados con fallback Redis
    def _existe_codigo_con_redis(self, codigo: str) -> bool:
        codigo_normalizado = codigo.strip().lower()
        
        # 1️⃣ Primero intentar verificar en Redis
        try:
            # Verificar en máquina individual
            if redis_client.exists(f"siglab:maquina:{codigo_normalizado}"):
                return True
                
            # Verificar en lista completa
            lista_cache = redis_client.get("siglab:maquinas:listar")
            if lista_cache:
                maquinas = json.loads(lista_cache)
                return any(str(m.get("codigo", "")).lower() == codigo_normalizado for m in maquinas)
                
        except Exception as redis_error:
            print(f"⚠️ Error verificando en Redis: {str(redis_error)}")
        
        # 2️⃣ Fallback a Base de Datos
        try:
            return self._existe_codigo(codigo)
        except Exception as db_error:
            print(f"⚠️ Error verificando en DB: {str(db_error)}")
            return False

    # Método auxiliar: Actualizar caché Redis con nueva máquina
    def _actualizar_cache_redis_con_nueva_maquina(self, nueva_maquina: dict):
        try:
            # Obtener lista actual
            lista_actual = redis_client.get("siglab:maquinas:listar")
            
            if lista_actual:
                maquinas = json.loads(lista_actual)
                maquinas.append(nueva_maquina)
            else:
                maquinas = [nueva_maquina]
            
            # Actualizar caché
            redis_client.setex("siglab:maquinas:listar", 60, json.dumps(maquinas))
            print("🔄 Caché Redis actualizada con nueva máquina")
            
        except Exception as e:
            print(f"⚠️ Error actualizando caché Redis: {str(e)}")

    # Método auxiliar: Fallback para obtener máquinas desde Redis
    def _obtener_maquinas_desde_redis_fallback(self) -> list:
        print("🔄 Modo resiliencia: Obteniendo máquinas desde Redis")
        
        try:
            # Intentar obtener lista completa
            lista_cache = redis_client.get("siglab:maquinas:listar")
            if lista_cache:
                return json.loads(lista_cache)
            
            # Si no hay lista, reconstruir desde máquinas individuales
            maquinas = []
            for key in redis_client.scan_iter(match="siglab:maquina:*"):
                datos_maquina = redis_client.get(key)
                if datos_maquina:
                    maquinas.append(json.loads(datos_maquina))
            
            if maquinas:
                # Guardar lista reconstruida
                redis_client.setex("siglab:maquinas:listar", 60, json.dumps(maquinas))
                print("🔄 Lista reconstruida desde máquinas individuales")
            
            return maquinas
            
        except Exception as e:
            print(f"❌ Error crítico en fallback Redis: {str(e)}")
            return []


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
