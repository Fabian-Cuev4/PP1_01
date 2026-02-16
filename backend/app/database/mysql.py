# Conexión MySQL - Gestión de base de datos y tablas

import mysql.connector
from mysql.connector import Error
import os

class MySQLConnection:
    # Variables de entorno con valores por defecto
    USER = os.getenv('MYSQL_USER', 'root')
    PASSWORD = os.getenv('MYSQL_PASSWORD', 'Clubpengui1')
    HOST = os.getenv('MYSQL_HOST', 'mysql')
    DATABASE = os.getenv('MYSQL_DATABASE', 'proyecto_maquinas')

    @staticmethod
    def inicializar_base_datos():
        # Inicializa BD y tablas con sistema de reintentos
        import time
        max_retries = 15
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                conn = mysql.connector.connect(
                    host=MySQLConnection.HOST,
                    user=MySQLConnection.USER,
                    password=MySQLConnection.PASSWORD,
                    connection_timeout=10, 
                    autocommit=False
                )
                cursor = conn.cursor()

                # Crear BD si no existe
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MySQLConnection.DATABASE}")
                cursor.execute(f"USE {MySQLConnection.DATABASE}")
                
                # Crear tabla usuarios
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_completo VARCHAR(100) NOT NULL,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        rol VARCHAR(20) DEFAULT 'admin'
                    )
                """)
                
                # Actualizar contraseña admin por defecto
                try:
                    from app.utils.encryption import Encryption
                    admin_password = Encryption.encriptar_password('admin123')
                    cursor.execute("UPDATE usuarios SET password = %s, nombre_completo = 'admin' WHERE username = 'admin'", (admin_password,))
                except:
                    pass
                
                # Crear tabla máquinas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS maquinas (
                        codigo VARCHAR(50) PRIMARY KEY,
                        tipo VARCHAR(20) NOT NULL,
                        estado VARCHAR(50) NOT NULL,
                        area VARCHAR(100) NOT NULL,
                        fecha DATE NOT NULL,
                        usuario VARCHAR(50)
                    )
                """)
                
                # Agregar columna usuario si no existe
                try:
                    cursor.execute("ALTER TABLE maquinas ADD COLUMN usuario VARCHAR(50)")
                except:
                    pass

                # Crear admin por defecto
                cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
                if not cursor.fetchone():
                    from app.utils.encryption import Encryption
                    admin_password = Encryption.encriptar_password('admin123')
                    cursor.execute("INSERT INTO usuarios (nombre_completo, username, password, rol) VALUES ('admin', 'admin', %s, 'admin')", (admin_password,))

                conn.commit()
                cursor.close()
                conn.close()
                return
            
            except (Error, Exception) as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise Exception(f"No se pudo conectar a MySQL tras muchos intentos.")

    # Pool de conexiones
    _pool = None

    @classmethod
    def get_pool(cls):
        # Administra pool de conexiones para rendimiento
        if cls._pool is None:
            try:
                print(f"DEBUG: Creando pool de conexiones con host={cls.HOST}, user={cls.USER}, database={cls.DATABASE}")
                cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=5,
                    pool_reset_session=True,
                    host=cls.HOST,
                    user=cls.USER,
                    password=cls.PASSWORD,
                    database=cls.DATABASE,
                    connection_timeout=5,
                    autocommit=False
                )
                print("DEBUG: Pool de conexiones creado exitosamente")
            except Error as e:
                print(f"DEBUG: Error creando pool de conexiones: {e}")
                return None
        return cls._pool

    @staticmethod
    def conectar():
        # Obtiene conexión del pool
        pool = MySQLConnection.get_pool()
        if not pool:
            return None
        
        try:
            conn = pool.get_connection()
            if conn.is_connected():
                return conn
            return None
        except Exception as e:
            return None