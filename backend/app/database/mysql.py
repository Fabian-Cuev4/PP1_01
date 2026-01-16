import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    # --- CONFIGURA ESTO ---
    USER = 'root'
    PASSWORD = 'Clubpengui1'  
    HOST = 'localhost'
    DATABASE = 'proyecto_maquinas'
    # ----------------------

    @staticmethod
    def inicializar_base_datos():
        try:
            # Intentamos entrar al servidor
            conn = mysql.connector.connect(
                host=MySQLConnection.HOST,
                user=MySQLConnection.USER,
                password=MySQLConnection.PASSWORD
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MySQLConnection.DATABASE}")
            cursor.execute(f"USE {MySQLConnection.DATABASE}")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS maquinas (
                    codigo VARCHAR(50) PRIMARY KEY,
                    tipo VARCHAR(20),
                    estado VARCHAR(50),
                    area VARCHAR(100),
                    fecha DATE
                )
            """)
            conn.commit()
            print("¡ÉXITO! MySQL configurado y base de datos lista. :V")
        except Error as e:
            print(f"ERROR DE ACCESO: Revisa si tu contraseña es correcta. Error: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def conectar():
        try:
            return mysql.connector.connect(
                host=MySQLConnection.HOST,
                user=MySQLConnection.USER,
                password=MySQLConnection.PASSWORD,
                database=MySQLConnection.DATABASE
            )
        except Error as e:
            return None