# DAO LIMPIO - Solo acceso a datos MySQL
# Responsabilidades: consultas SQL puras, sin lógica de negocio

from app.database.mysql import MySQLConnection
from app.utils.encryption import Encryption

class UsuarioDAO:
    # Inserta un usuario con datos primitivos
    def insertar(self, nombre_completo: str, username: str, password: str, rol: str = "usuario") -> bool:
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            password_encriptado = Encryption.encriptar_password(password)
            query = """
                INSERT INTO usuarios (nombre_completo, username, password, rol) 
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(query, (nombre_completo, username, password_encriptado, rol))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            return False

    # Guarda usuario usando objeto Usuario (compatibilidad)
    def guardar(self, usuario) -> bool:
        return self.insertar(
            usuario.nombre_completo,
            usuario.username,
            usuario.password,
            usuario.rol
        )

    # Verifica credenciales de usuario
    def verificar_credenciales(self, username: str, password: str) -> dict:
        conn = MySQLConnection.conectar()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if usuario and Encryption.verificar_password(password, usuario['password']):
                return usuario
            return None
        except Exception as e:
            print(f"Error en verificar_credenciales: {e}")
            return None

    # Obtiene usuario por username
    def obtener_por_username(self, username: str) -> dict:
        conn = MySQLConnection.conectar()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return resultado
        except Exception:
            return None

    # Método legacy para compatibilidad
    def obtener_usuario_por_username(self, username: str) -> dict:
        return self.obtener_por_username(username)

    # Crea usuario con datos primitivos (método legacy)
    def crear_usuario(self, nombre_completo: str, username: str, password: str, rol: str = "usuario") -> bool:
        return self.insertar(nombre_completo, username, password, rol)
