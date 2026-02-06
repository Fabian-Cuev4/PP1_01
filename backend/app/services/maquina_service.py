# Este archivo se encarga de la lógica de negocio de máquinas
# Service es el cerebro: aquí validamos y coordinamos las operaciones

# Importamos las clases necesarias
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora

class MaquinaService:
    # Esta clase coordina todas las operaciones de máquinas (PC e IMP)
    
    def __init__(self, maquina_dao):
        # Guardamos la referencia al DAO para usarla después
        self._maquina_dao = maquina_dao
    
    def registrar_maquina(self, datos_dict):
        # Esta función registra una nueva máquina en el sistema
        
        print(f"DEBUG: registrar_maquina recibido: {datos_dict}")
        print(f"DEBUG: tipo_equipo: {datos_dict.get('tipo_equipo')}")
        print(f"DEBUG: codigo_equipo: {datos_dict.get('codigo_equipo')}")
        
        # Validación: el código es obligatorio
        codigo = datos_dict.get("codigo_equipo")
        if not codigo or codigo.strip() == "":
            print("DEBUG: Código vacío")
            return None, "El código de la máquina es obligatorio"
        
        # Validación: el código debe ser único
        maquina_existente = self._maquina_dao.buscar_por_codigo(codigo)
        if maquina_existente:
            return None, f"El código '{codigo}' ya existe"
        
        # Validación: el tipo es obligatorio y debe ser exactamente PC o IMP
        tipo = datos_dict.get("tipo_equipo", "").upper()
        if not tipo:
            return None, "El tipo de equipo es obligatorio"
        
        if tipo not in ["PC", "IMP"]:
            return None, "El tipo de equipo debe ser exactamente PC o IMP"
        
        # Validación: otros campos obligatorios
        if not datos_dict.get("estado_actual"):
            return None, "El estado actual es obligatorio"
        
        if not datos_dict.get("area"):
            return None, "El área es obligatoria"
        
        if not datos_dict.get("usuario"):
            return None, "El usuario es obligatorio"
        
        # Creamos el objeto máquina según su tipo (sin normalización)
        try:
            if tipo == "PC":
                nueva_maquina = Computadora(
                    codigo,
                    datos_dict.get("estado_actual"),
                    datos_dict.get("area"),
                    datos_dict.get("fecha"),
                    datos_dict.get("usuario")
                )
            elif tipo == "IMP":
                nueva_maquina = Impresora(
                    codigo,
                    datos_dict.get("estado_actual"),
                    datos_dict.get("area"),
                    datos_dict.get("fecha"),
                    datos_dict.get("usuario")
                )
            
            # Guardamos la máquina en la base de datos
            resultado = self._maquina_dao.guardar(nueva_maquina)
            print(f"DEBUG: Resultado de guardar: {resultado}")
            
            if resultado:
                return nueva_maquina, "Máquina registrada correctamente"
            else:
                return None, "Error al guardar la máquina"
            
        except Exception as e:
            return None, f"Error al guardar la máquina: {str(e)}"
    
    def actualizar_maquina(self, datos_dict):
        # Esta función actualiza los datos de una máquina existente
        
        print(f"DEBUG: actualizar_maquina recibido: {datos_dict}")
        
        # Validación: el código es obligatorio
        codigo = datos_dict.get("codigo_equipo")
        if not codigo or codigo.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        maquina_db = self._maquina_dao.buscar_por_codigo(codigo)
        if not maquina_db:
            return None, f"La máquina '{codigo}' no existe"
        
        # Validación: si se proporciona tipo, debe ser exactamente PC o IMP
        tipo = datos_dict.get("tipo_equipo", "").upper()
        print(f"DEBUG: tipo recibido: {tipo}")
        
        if tipo and tipo not in ["PC", "IMP"]:
            print(f"DEBUG: tipo no válido: {tipo}")
            return None, "El tipo de equipo debe ser exactamente PC o IMP"
        
        # Si no se proporciona tipo, usamos el existente
        if not tipo:
            tipo = maquina_db.get('tipo', '').upper()
            print(f"DEBUG: tipo existente en DB: {tipo}")
            # Normalizamos el tipo existente para compatibilidad
            if tipo in ["COMPUTADORA"]:
                tipo = "PC"
            elif tipo in ["IMPRESORA"]:
                tipo = "IMP"
            elif tipo not in ["PC", "IMP"]:
                print(f"DEBUG: tipo existente no válido: {tipo}")
                return None, "El tipo de equipo existente debe ser PC o IMP"
        
        # Obtenemos los datos (nuevos o existentes)
        estado = datos_dict.get("estado_actual") or maquina_db.get('estado')
        area = datos_dict.get("area") or maquina_db.get('area')
        fecha = datos_dict.get("fecha") or maquina_db.get('fecha')
        usuario = datos_dict.get("usuario") or maquina_db.get('usuario')
        
        # Creamos el objeto máquina actualizado
        try:
            print(f"DEBUG: Creando objeto máquina con tipo: {tipo}")
            if tipo == "PC":
                maquina_obj = Computadora(codigo, estado, area, fecha, usuario)
            elif tipo == "IMP":
                maquina_obj = Impresora(codigo, estado, area, fecha, usuario)
            
            print(f"DEBUG: Objeto creado, actualizando en DB...")
            # Actualizamos en la base de datos
            resultado = self._maquina_dao.actualizar(maquina_obj)
            print(f"DEBUG: Resultado de actualización: {resultado}")
            
            if resultado:
                return maquina_obj, "Máquina actualizada correctamente"
            else:
                return None, "Error al actualizar la máquina"
                
        except Exception as e:
            return None, f"Error al actualizar la máquina: {str(e)}"
    
    def eliminar_maquina(self, codigo):
        # Esta función elimina una máquina
        
        # Validación: el código es obligatorio
        if not codigo or codigo.strip() == "":
            return False, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        if not self._maquina_dao.buscar_por_codigo(codigo):
            return False, f"La máquina '{codigo}' no existe"
        
        # Eliminamos la máquina
        if self._maquina_dao.eliminar(codigo):
            return True, "Máquina eliminada correctamente"
        else:
            return False, "Error al eliminar la máquina"
    
    def obtener_maquina(self, codigo):
        # Esta función obtiene los datos de una máquina
        
        # Validación: el código es obligatorio
        if not codigo or codigo.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Buscamos la máquina
        maquina = self._maquina_dao.buscar_por_codigo(codigo)
        
        if maquina:
            return maquina, None
        else:
            return None, f"La máquina '{codigo}' no existe"
    
    def listar_todas_las_maquinas(self):
        # Esta función obtiene todas las máquinas
        try:
            return self._maquina_dao.listar_todas(), None
        except Exception as e:
            return [], f"Error al listar máquinas: {str(e)}"
    
    def buscar_maquinas_por_codigo(self, codigo_parcial):
        # Esta función busca máquinas por código parcial
        try:
            todas_las_maquinas = self._maquina_dao.listar_todas()
            
            if not codigo_parcial:
                return todas_las_maquinas, None
            
            # Filtramos las máquinas que contienen el código parcial
            codigo_buscar = str(codigo_parcial).strip().lower()
            maquinas_filtradas = []
            
            for maquina in todas_las_maquinas:
                codigo_maq = str(maquina.get("codigo", "")).lower()
                if codigo_buscar in codigo_maq:
                    maquinas_filtradas.append(maquina)
            
            return maquinas_filtradas, None
            
        except Exception as e:
            return [], f"Error al buscar máquinas: {str(e)}"
