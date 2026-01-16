import mysql.connector
from mysql.connector import Error

import os

class MySQLConnection:
    # --- CONFIGURA ESTO ---
    USER = os.getenv('MYSQL_USER', 'root')
    PASSWORD = os.getenv('MYSQL_PASSWORD', 'Clubpengui1')
    HOST = os.getenv('MYSQL_HOST', 'mysql')
    DATABASE = os.getenv('MYSQL_DATABASE', 'proyecto_maquinas')
    # ----------------------

    @staticmethod
    def inicializar_base_datos():
        import time
        max_retries = 15  # Aumentado para dar más tiempo
        retry_delay = 3  # Aumentado el delay entre intentos
        
        for attempt in range(max_retries):
            try:
                # Intentamos entrar al servidor con timeout más largo
                conn = mysql.connector.connect(
                    host=MySQLConnection.HOST,
                    user=MySQLConnection.USER,
                    password=MySQLConnection.PASSWORD,
                    connection_timeout=10,  # Aumentado timeout
                    autocommit=False
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
                cursor.close()
                conn.close()
                return
            except Error as e:
                if attempt < max_retries - 1:
                    print(f"Intento {attempt + 1}/{max_retries} fallido. Reintentando en {retry_delay} segundos... Error: {e}")
                    time.sleep(retry_delay)
                else:
                    print(f"ERROR DE ACCESO después de {max_retries} intentos: {e}")
                    # No lanzamos excepción, permitimos que la app continúe
                    # El sistema de reintentos del backend manejará esto
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Intento {attempt + 1}/{max_retries} fallido. Reintentando en {retry_delay} segundos... Error: {e}")
                    time.sleep(retry_delay)
                else:
                    print(f"ERROR después de {max_retries} intentos: {e}")
                    # No lanzamos excepción, permitimos que la app continúe

    @staticmethod
    def conectar():
        import time
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                conn = mysql.connector.connect(
                    host=MySQLConnection.HOST,
                    user=MySQLConnection.USER,
                    password=MySQLConnection.PASSWORD,
                    database=MySQLConnection.DATABASE,
                    connection_timeout=5,
                    autocommit=False
                )
                # Verificar que la conexión funciona
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                return conn
            except Error as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print(f"Error al conectar a MySQL después de {max_retries} intentos: {e}")
                    return None
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print(f"Error inesperado al conectar a MySQL: {e}")
                    return None
        return None