# Este archivo es el DAO para las Máquinas.
# Maneja todo lo relacionado con el inventario de equipos en la base de datos MySQL.

from app.database.mysql import MySQLConnection

class MaquinaDAO:
    
    def guardar(self, maquina):
        
        #Recibe un objeto de tipo Máquina y lo guarda en MySQL. 
        conn = MySQLConnection.conectar()
        if not conn: return
        
        try:
            cursor = conn.cursor()
            # La orden SQL para insertar o actualizar los datos de la máquina
            query = """
                INSERT INTO maquinas (codigo, tipo, estado, area, fecha) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                maquina.codigo_equipo, 
                maquina.tipo_equipo, 
                maquina.estado_actual, 
                maquina.area, 
                maquina.fecha
            ))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al guardar máquina: {e}")
            raise e

    def buscar_por_codigo(self, codigo):
        
        #Busca si existe una máquina con el código indicado (Exacto).
        conn = MySQLConnection.conectar()
        if not conn: return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM maquinas WHERE LOWER(codigo) = LOWER(%s)"
            cursor.execute(query, (codigo.strip().lower(),))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return resultado
        except Exception as e:
            print(f"Error al buscar máquina: {e}")
            return None


    def listar_todas(self):
        #Trae una lista de TODAS las máquinas registradas en el sistema.
        conn = MySQLConnection.conectar()
        if not conn: return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM maquinas")
            lista = cursor.fetchall() # fetchall() trae todas las filas
            cursor.close()
            conn.close()
            return lista
        except Exception as e:
            print(f"Error al listar máquinas: {e}")
            return []
