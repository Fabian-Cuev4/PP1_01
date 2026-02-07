# Guarda y busca usuarios en base de datos MySQL
# DAO significa "Data Access Object" - Objeto de Acceso a Datos
# Su única función es ejecutar SQL puro, sin lógica de negocio

# Importamos clases necesarias
from app.database.mysql import MySQLConnection

class UsuarioDAO:
    # Crea nuevo usuario en base de datos
    # Recibe contraseña ya encriptada (sin encriptar aquí)
    @staticmethod
    def crear_usuario(nombre, username, password_encriptado):
        # Obtenemos conexión a base de datos
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            # Creamos cursor para ejecutar comandos SQL
            cursor = conn.cursor()
            # Definimos consulta SQL para insertar usuario
            query = "INSERT INTO usuarios (nombre_completo, username, password) VALUES (%s, %s, %s)"
            # Ejecutamos consulta con datos (contraseña ya encriptada)
            cursor.execute(query, (nombre, username, password_encriptado))
            # Confirmamos cambios
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            # Cerramos cursor y conexión siempre
            cursor.close()
            conn.close()

    # Obtiene usuario por su nombre de usuario
    @staticmethod
    def obtener_usuario_por_username(username):
        # Obtenemos conexión a base de datos
        conn = MySQLConnection.conectar()
        if not conn:
            return None
        
        try:
            # Creamos cursor que retorna diccionarios
            cursor = conn.cursor(dictionary=True)
            # Buscamos usuario por nombre de usuario
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            # Obtenemos primer resultado (si existe)
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None
        finally:
            # Cerramos cursor y conexión siempre
            if conn.is_connected():
                cursor.close()
                conn.close()
