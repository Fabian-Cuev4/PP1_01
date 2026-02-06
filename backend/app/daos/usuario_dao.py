# Este archivo se encarga de guardar y buscar usuarios en la base de datos MySQL
# DAO significa "Data Access Object" (Objeto de Acceso a Datos)
# Su única función es ejecutar SQL puro, sin lógica de negocio

# Importamos las clases necesarias
from app.database.mysql import MySQLConnection

class UsuarioDAO:
    # Esta función crea un nuevo usuario en la base de datos
    # Recibe la contraseña ya encriptada (sin encriptar aquí)
    @staticmethod
    def crear_usuario(nombre, username, password_encriptado):
        # Obtenemos una conexión a la base de datos
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            # Creamos un cursor para ejecutar comandos SQL
            cursor = conn.cursor()
            # Definimos la consulta SQL para insertar un usuario
            query = "INSERT INTO usuarios (nombre_completo, username, password) VALUES (%s, %s, %s)"
            # Ejecutamos la consulta pasándole los datos (la contraseña ya viene encriptada)
            cursor.execute(query, (nombre, username, password_encriptado))
            # Confirmamos los cambios
            conn.commit()
            return True
        except Exception as e:
            # Si hay un error (por ejemplo, el usuario ya existe), lo imprimimos
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            # Siempre cerramos el cursor y la conexión, aunque haya un error
            cursor.close()
            conn.close()

    # Esta función obtiene un usuario por su nombre de usuario
    @staticmethod
    def obtener_usuario_por_username(username):
        # Obtenemos una conexión a la base de datos
        conn = MySQLConnection.conectar()
        if not conn:
            return None
        
        try:
            # Creamos un cursor que retorna diccionarios
            cursor = conn.cursor(dictionary=True)
            # Buscamos el usuario por su nombre de usuario
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            # Obtenemos el primer resultado (si existe)
            return cursor.fetchone()
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos None
            print(f"Error al buscar usuario: {e}")
            return None
        finally:
            # Siempre cerramos el cursor y la conexión
            if conn.is_connected():
                cursor.close()
                conn.close()
