from app.database.mysql import MySQLConnection

class MaquinaDAO:
    def guardar(self, maquina):
        conn = MySQLConnection.conectar()
        if not conn: return
        try:
            cursor = conn.cursor()
            query = """INSERT INTO maquinas (codigo, tipo, estado, area, fecha) 
                       VALUES (%s, %s, %s, %s, %s)"""
            valores = (maquina.codigo_equipo, maquina.tipo_maquina, 
                       maquina.estado_actual, maquina.area, maquina.fecha)
            cursor.execute(query, valores)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def buscar_por_codigo(self, codigo):
        conn = MySQLConnection.conectar()
        if not conn: return None
        try:
            # dictionary=True sirve para que devuelva un JSON (dict) y no una lista
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM maquinas WHERE codigo = %s", (codigo,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # --- ESTA ES LA FUNCIÓN QUE TE FALTA ---
    def listar_todas(self):
        conn = MySQLConnection.conectar()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT codigo, tipo, estado, area, fecha FROM maquinas")
            resultado = cursor.fetchall()
            # Convertimos la fecha a string para que FastAPI no sufra al enviarla al front
            for r in resultado:
                if r['fecha']:
                    r['fecha'] = str(r['fecha'])
            return resultado
        finally:
            cursor.close()
            conn.close()