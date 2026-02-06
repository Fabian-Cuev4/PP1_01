# Este archivo se encarga de la lógica de negocio de mantenimientos
# Service es el cerebro: aquí validamos y coordinamos las operaciones

# Importamos las clases necesarias
from app.models.Mantenimiento import Mantenimiento
from app.models.Computadora import Computadora
from app.models.Impresora import Impresora

class MantenimientoService:
    # Esta clase coordina todas las operaciones de mantenimientos
    
    def __init__(self, mantenimiento_dao, maquina_dao):
        # Guardamos las referencias a los DAOs para usarlos después
        self._mantenimiento_dao = mantenimiento_dao
        self._maquina_dao = maquina_dao
    
    def registrar_mantenimiento(self, datos_dict):
        # Esta función registra un nuevo mantenimiento con todas las validaciones
        
        # Validación: el código de máquina es obligatorio
        codigo_maquina = datos_dict.get("codigo_maquina")
        if not codigo_maquina or codigo_maquina.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        maquina_db = self._maquina_dao.buscar_por_codigo(codigo_maquina)
        if not maquina_db:
            return None, f"La máquina '{codigo_maquina}' no existe"
        
        # Validación: campos obligatorios
        if not datos_dict.get("empresa"):
            return None, "La empresa es obligatoria"
        
        if not datos_dict.get("tecnico"):
            return None, "El técnico es obligatorio"
        
        if not datos_dict.get("tipo"):
            return None, "El tipo de mantenimiento es obligatorio"
        
        if not datos_dict.get("fecha"):
            return None, "La fecha es obligatoria"
        
        if not datos_dict.get("usuario"):
            return None, "El usuario que registra es obligatorio"
        
        # Creamos el objeto máquina según su tipo
        tipo_maquina = maquina_db.get('tipo', '').upper()
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
            return None, "Tipo de máquina no reconocido"
        
        # Usamos el usuario del mantenimiento o el de la máquina
        usuario = datos_dict.get("usuario") or maquina_db.get('usuario')
        
        # Creamos el objeto mantenimiento
        try:
            nuevo_mantenimiento = Mantenimiento(
                maquina_objeto=maquina_obj,
                empresa=datos_dict.get("empresa"),
                tecnico=datos_dict.get("tecnico"),
                tipo=datos_dict.get("tipo"),
                fecha=datos_dict.get("fecha"),
                observaciones=datos_dict.get("observaciones", ""),
                usuario=usuario
            )
            
            # Guardamos el mantenimiento
            resultado = self._mantenimiento_dao.guardar(nuevo_mantenimiento)
            print(f"DEBUG: Resultado de guardar mantenimiento: {resultado}")
            
            if resultado:
                return nuevo_mantenimiento, "Mantenimiento registrado correctamente"
            else:
                return None, "Error al guardar el mantenimiento"
            
        except Exception as e:
            return None, f"Error al guardar el mantenimiento: {str(e)}"
    
    def obtener_historial_por_maquina(self, codigo_maquina):
        # Esta función obtiene todos los mantenimientos de una máquina
        
        # Validación: el código es obligatorio
        if not codigo_maquina or codigo_maquina.strip() == "":
            return None, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        if not self._maquina_dao.buscar_por_codigo(codigo_maquina):
            return None, f"La máquina '{codigo_maquina}' no existe"
        
        # Obtenemos el historial
        try:
            historial = self._mantenimiento_dao.listar_por_maquina(codigo_maquina)
            return historial, None
        except Exception as e:
            return None, f"Error al obtener el historial: {str(e)}"
    
    def obtener_todos_los_mantenimientos(self):
        # Esta función obtiene todos los mantenimientos del sistema
        try:
            return self._mantenimiento_dao.listar_todos(), None
        except Exception as e:
            return [], f"Error al listar mantenimientos: {str(e)}"
    
    def eliminar_mantenimientos_por_maquina(self, codigo_maquina):
        # Esta función elimina todos los mantenimientos de una máquina
        
        # Validación: el código es obligatorio
        if not codigo_maquina or codigo_maquina.strip() == "":
            return False, "El código de la máquina es obligatorio"
        
        # Verificamos que la máquina exista
        if not self._maquina_dao.buscar_por_codigo(codigo_maquina):
            return False, f"La máquina '{codigo_maquina}' no existe"
        
        # Eliminamos los mantenimientos
        try:
            cantidad_eliminada = self._mantenimiento_dao.eliminar_por_maquina(codigo_maquina)
            return True, f"Se eliminaron {cantidad_eliminada} mantenimientos"
        except Exception as e:
            return False, f"Error al eliminar mantenimientos: {str(e)}"
    
    def obtener_informe_completo(self, codigo_maquina=None):
        # Esta función genera un reporte completo de máquinas y mantenimientos
        
        try:
            # Obtenemos todas las máquinas
            todas_las_maquinas = self._maquina_dao.listar_todas()
            
            # Si nos dieron un código, filtramos solo esa máquina
            if codigo_maquina:
                codigo_buscar = str(codigo_maquina).strip().lower()
                maquinas_filtradas = []
                for maquina in todas_las_maquinas:
                    codigo_maq = str(maquina.get("codigo", "")).lower()
                    if codigo_buscar in codigo_maq:
                        maquinas_filtradas.append(maquina)
                maquinas_db = maquinas_filtradas
            else:
                maquinas_db = todas_las_maquinas
            
            # Si no hay máquinas, retornamos lista vacía
            if not maquinas_db:
                return [], None
            
            # Obtenemos todos los mantenimientos
            todos_mantenimientos = self._mantenimiento_dao.listar_todos() or []
            
            # Agrupamos mantenimientos por código de máquina
            mantenimientos_por_maquina = {}
            for mantenimiento in todos_mantenimientos:
                codigo_mt = mantenimiento.get("codigo_maquina") or mantenimiento.get("codigo")
                if codigo_mt:
                    codigo_key = str(codigo_mt).strip().lower()
                    if codigo_key not in mantenimientos_por_maquina:
                        mantenimientos_por_maquina[codigo_key] = []
                    
                    # Convertimos el ID de MongoDB a string
                    if "_id" in mantenimiento:
                        mantenimiento["_id"] = str(mantenimiento["_id"])
                    
                    # Si no tiene tipo, le ponemos "N/A"
                    if "tipo" not in mantenimiento:
                        mantenimiento["tipo"] = "N/A"
                    
                    mantenimientos_por_maquina[codigo_key].append(mantenimiento)
            
            # Construimos el reporte final
            resultado = []
            for maquina in maquinas_db:
                codigo_maq = str(maquina.get("codigo", "")).strip().lower()
                mantenimientos = mantenimientos_por_maquina.get(codigo_maq, [])
                
                resultado.append({
                    "codigo": maquina["codigo"],
                    "tipo": maquina["tipo"],
                    "area": maquina["area"],
                    "estado": maquina["estado"],
                    "mantenimientos": mantenimientos
                })
            
            return resultado, None
            
        except Exception as e:
            return [], f"Error al generar informe: {str(e)}"
