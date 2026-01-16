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
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_completo VARCHAR(100) NOT NULL,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    rol VARCHAR(20) DEFAULT 'estudiante'
                )
            """)
            # ----------------------------------

            # Insertamos un admin por defecto si no existe (para que Javier pueda entrar ya)
            cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
            if not cursor.fetchone():
                cursor.execute("INSERT INTO usuarios (nombre_completo, username, password, rol) VALUES ('Administrador', 'admin', '12345', 'admin')")

            conn.commit()
            print("¡ÉXITO! MySQL configurado (Máquinas y Usuarios) listo. :V")
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