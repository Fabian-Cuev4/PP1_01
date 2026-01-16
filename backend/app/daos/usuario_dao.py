# Este archivo es el DAO (Data Access Object) para Usuarios.
# Su misión es hablar con la base de datos MySQL para guardar o buscar usuarios.

from app.database.mysql import MySQLConnection

class UsuarioDAO:
    
    @staticmethod
    def crear_usuario(nombre, username, password):
        
        #Guarda un nuevo usuario en la tabla 'usuarios' de MySQL.
        
        # Abrimos conexión con la base de datos MySQL
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            # Es el encargado de ejecutar las órdenes de SQL
            cursor = conn.cursor()
            # Definimos la orden (INSERT) y usamos %s para que sea seguro
            query = "INSERT INTO usuarios (nombre_completo, username, password) VALUES (%s, %s, %s)"
            # Ejecutamos pasándole los datos reales
            cursor.execute(query, (nombre, username, password))
            # Confirmamos que queremos guardar los cambios (Commit)
            conn.commit()
            return True
        except Exception as e:
            # Si hay un error (ej. usuario ya existe), lo mostramos en consola
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            # Siempre cerramos todo para no dejar conexiones abiertas
            cursor.close()
            conn.close()

    @staticmethod
    def verificar_credenciales(username, password):
        
        #Busca un usuario por su nombre y clave para dejarlo entrar al sistema.
        conn = MySQLConnection.conectar()
        if not conn:
            return None
        
        try:
            # dictionary=True hace que el resultado sea fácil de leer (como un objeto JSON)
            cursor = conn.cursor(dictionary=True) 
            query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            # Traemos el primer resultado que coincida
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            print(f"Error en login: {e}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
