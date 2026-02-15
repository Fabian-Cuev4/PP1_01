# Este archivo se encarga de guardar y buscar usuarios en la base de datos MySQL
# DAO significa "Data Access Object" (Objeto de Acceso a Datos)

# Importamos las clases necesarias
from app.database.mysql import MySQLConnection
from app.utils.encryption import Encryption
from app.models.Usuario import Usuario

class UsuarioDAO:
    # Esta función guarda un usuario usando el objeto Usuario
    @staticmethod
    def guardar(usuario):
        try:
            # Validamos los datos del usuario
            usuario.validar_datos()
            
            # Obtenemos una conexión a la base de datos
            conn = MySQLConnection.conectar()
            if not conn:
                return False
            
            # Encriptamos la contraseña antes de guardarla por seguridad
            password_encriptado = Encryption.encriptar_password(usuario.password)
            
            # Creamos un cursor para ejecutar comandos SQL
            cursor = conn.cursor()
            # Definimos la consulta SQL para insertar un usuario
            query = "INSERT INTO usuarios (nombre_completo, username, password, rol) VALUES (%s, %s, %s, %s)"
            # Ejecutamos la consulta pasándole los datos
            cursor.execute(query, (
                usuario.nombre_completo, 
                usuario.username, 
                password_encriptado, 
                usuario.rol
            ))
            # Confirmamos los cambios
            conn.commit()
            return True
        except ValueError as e:
            return False
        except Exception as e:
            return False
        finally:
            # Siempre cerramos el cursor y la conexión
            cursor.close()
            conn.close()

    # Esta función crea un nuevo usuario en la base de datos (método legacy)
    @staticmethod
    def crear_usuario(nombre_completo, username, password, rol="usuario"):
        try:
            # Creamos el objeto usuario y validamos los datos
            usuario = Usuario(nombre_completo, username, password, rol)
            usuario.validar_datos()  # Lanza excepción si hay error
            
            # Obtenemos una conexión a la base de datos
            conn = MySQLConnection.conectar()
            if not conn:
                return False
            
            # Encriptamos la contraseña antes de guardarla por seguridad
            password_encriptado = Encryption.encriptar_password(password)
            
            # Creamos un cursor para ejecutar comandos SQL
            cursor = conn.cursor()
            # Definimos la consulta SQL para insertar un usuario
            query = "INSERT INTO usuarios (nombre_completo, username, password, rol) VALUES (%s, %s, %s, %s)"
            # Ejecutamos la consulta pasándole los datos
            cursor.execute(query, (nombre_completo, username, password_encriptado, rol))
            # Confirmamos los cambios
            conn.commit()
            return True
        except ValueError as e:
            return False
        except Exception as e:
            return False
        finally:
            # Siempre cerramos el cursor y la conexión, aunque haya un error
            cursor.close()
            conn.close()

    # Esta función verifica si el usuario y contraseña son correctos
    @staticmethod
    def verificar_credenciales(username, password):
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
            usuario = cursor.fetchone()
            
            # Si encontramos el usuario, verificamos la contraseña
            if usuario and Encryption.verificar_password(password, usuario['password']):
                # Si la contraseña es correcta, retornamos los datos del usuario
                return usuario
            # Si no encontramos el usuario o la contraseña es incorrecta, retornamos None
            return None
        except Exception as e:
            return None
        finally:
            # Siempre cerramos el cursor y la conexión
            if conn.is_connected():
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
            return None
        finally:
            # Siempre cerramos el cursor y la conexión
            if conn.is_connected():
                cursor.close()
                conn.close()
