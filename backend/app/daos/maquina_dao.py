# DAO LIMPIO - Solo acceso a datos MySQL
# Responsabilidades: consultas SQL puras, sin lógica de negocio

from app.database.mysql import MySQLConnection

class MaquinaDAO:
    # Inserta una máquina con datos primitivos
    def insertar(self, codigo: str, tipo: str, estado: str, area: str, fecha: str, usuario: str = None) -> bool:
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO maquinas (codigo, tipo, estado, area, fecha, usuario) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, (codigo, tipo, estado, area, fecha, usuario))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            return False

    # Actualiza una máquina con datos primitivos
    def actualizar(self, codigo: str, tipo: str, estado: str, area: str, fecha: str, usuario: str = None) -> bool:
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = """
                UPDATE maquinas 
                SET tipo = %s, estado = %s, area = %s, fecha = %s, usuario = %s
                WHERE codigo = %s
                """
            cursor.execute(query, (tipo, estado, area, fecha, usuario, codigo))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            return False

    # Elimina una máquina por código exacto
    def eliminar(self, codigo: str) -> bool:
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = "DELETE FROM maquinas WHERE codigo = %s"
            cursor.execute(query, (codigo,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            return False

    # Busca por código exacto (case-sensitive)
    def buscar_por_codigo_exacto(self, codigo: str) -> dict:
        conn = MySQLConnection.conectar()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM maquinas WHERE codigo = %s"
            cursor.execute(query, (codigo,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return resultado
        except Exception:
            return None

    # Obtiene todas las máquinas sin filtrar
    def listar_todas(self) -> list:
        conn = MySQLConnection.conectar()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM maquinas")
            lista = cursor.fetchall()
            cursor.close()
            conn.close()
            return lista
        except Exception:
            return []

    # Busca con filtro LIKE (para búsquedas parciales)
    def buscar_similares(self, codigo_parcial: str) -> list:
        conn = MySQLConnection.conectar()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM maquinas WHERE codigo LIKE %s"
            cursor.execute(query, (f"%{codigo_parcial}%",))
            lista = cursor.fetchall()
            cursor.close()
            conn.close()
            return lista
        except Exception:
            return []
