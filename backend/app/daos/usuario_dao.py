from app.database.mysql import MySQLConnection

class UsuarioDAO:
    
    @staticmethod
    def crear_usuario(nombre, username, password):
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = "INSERT INTO usuarios (nombre_completo, username, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, username, password))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def verificar_credenciales(username, password):
        conn = MySQLConnection.conectar()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True) # dictionary=True devuelve un JSON bonito
            query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            print(f"Error en login: {e}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()