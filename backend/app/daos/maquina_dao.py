from app.database.mysql import MySQLConnection

class MaquinaDAO:
    def guardar(self, maquina):
        conn = MySQLConnection.conectar()
        if not conn: return
        try:
            cursor = conn.cursor()
            query = "INSERT INTO maquinas (codigo, tipo, estado, area, fecha) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (maquina.codigo_equipo, maquina.tipo_maquina, 
                                   maquina.estado_actual, maquina.area, maquina.fecha))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def buscar_por_codigo(self, codigo):
        conn = MySQLConnection.conectar()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM maquinas WHERE codigo = %s", (codigo,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def listar_todas(self):
        conn = MySQLConnection.conectar()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM maquinas")
            res = cursor.fetchall()
            for r in res:
                if r['fecha']: r['fecha'] = str(r['fecha'])
            return res
        finally:
            cursor.close()
            conn.close()