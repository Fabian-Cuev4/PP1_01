# Este archivo es el corazón de la conexión con MySQL.
# Se encarga de abrir la puerta a la base de datos y crear las tablas necesarias.

import mysql.connector
from mysql.connector import Error
import os

class MySQLConnection:
    # Usamos os.getenv para leer variables del sistema (especialmente en Docker)
    # Si no existen, usamos unos valores por defecto.
    USER = os.getenv('MYSQL_USER', 'root')
    PASSWORD = os.getenv('MYSQL_PASSWORD', 'Clubpengui1')
    HOST = os.getenv('MYSQL_HOST', 'mysql_db')  # EXPLICACIÓN: Actualizado para Docker
    DATABASE = os.getenv('MYSQL_DATABASE', 'proyecto_maquinas')

    @staticmethod
    def inicializar_base_datos():
        
        #Esta función se asegura de que la base de datos y las tablas existan al arrancar.
        #Tiene un sistema de 'reintentos' por si MySQL tarda en encender.
        
        import time
        max_retries = 15  # Intentaremos conectar hasta 15 veces
        retry_delay = 3   # Esperaremos 3 segundos entre cada intento
        
        for attempt in range(max_retries):
            try:
                # EXPLICACIÓN: Log de intento de conexión al archivador central MySQL
                print(f"🔌 Intentando conectar al archivador central MySQL (intento {attempt + 1}/{max_retries})...")
                
                # Intentamos entrar al servidor de MySQL (sin especificar base de datos todavía)
                conn = mysql.connector.connect(
                    host=MySQLConnection.HOST,
                    user=MySQLConnection.USER,
                    password=MySQLConnection.PASSWORD,
                    connection_timeout=10, 
                    autocommit=False
                )
                cursor = conn.cursor()

                # Creamos la base de datos si no existe
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MySQLConnection.DATABASE}")
                # Empezamos a usar nuestra base de datos
                cursor.execute(f"USE {MySQLConnection.DATABASE}")

                # Creamos la tabla de usuarios
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_completo VARCHAR(100) NOT NULL,
                        username VARCHAR(50) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        rol VARCHAR(20) DEFAULT 'admin'
                    )
                """)
                
                # Actualizamos la contraseña del admin por defecto si existe (encriptada)
                try:
                    from app.utils.encryption import Encryption
                    admin_password = Encryption.encriptar_password('admin123')
                    cursor.execute("UPDATE usuarios SET password = %s, nombre_completo = 'admin' WHERE username = 'admin'", (admin_password,))
                except:
                    pass
                
                # Creamos la tabla de máquinas
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
                
                # Agregamos la columna usuario si no existe (para bases de datos antiguas)
                try:
                    cursor.execute("ALTER TABLE maquinas ADD COLUMN usuario VARCHAR(50)")
                except:
                    pass  # La columna ya existe

                # Creamos un administrador por defecto
                cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
                if not cursor.fetchone():
                    from app.utils.encryption import Encryption
                    admin_password = Encryption.encriptar_password('admin123')
                    cursor.execute("INSERT INTO usuarios (nombre_completo, username, password, rol) VALUES ('admin', 'admin', %s, 'admin')", (admin_password,))

                # Guardamos los cambios
                conn.commit()
                print("✅ ¡Conectado exitosamente al archivador central (MySQL)!")
                
                # Cerramos la conexión temporal
                cursor.close()
                conn.close()
                return # Salimos de la función con éxito
            
            except (Error, Exception) as e:
                # Si falla, esperamos un poco y volvemos a intentar
                if attempt < max_retries - 1:
                    print(f"❌ Intento {attempt + 1}/{max_retries} fallido. Reintentando... Error: {e}")
                    time.sleep(retry_delay)
                else:
                    print(f"🚫 ERROR: No se pudo conectar al archivador central MySQL tras muchos intentos.")

    # El 'Pool' es como una reserva de conexiones abiertas para no tener que abrir una nueva cada vez.
    _pool = None

    @classmethod
    def get_pool(cls):
        
        #Administra una piscina de conexiones para que el servidor sea más rápido.
        
        if cls._pool is None:
            try:
                cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=5, # Mantenemos 5 conexiones listas siempre
                    pool_reset_session=True,
                    host=cls.HOST,
                    user=cls.USER,
                    password=cls.PASSWORD,
                    database=cls.DATABASE,
                    connection_timeout=5,
                    autocommit=False
                )
            except Error as e:
                print(f"Error al crear el pool: {e}")
                return None
        return cls._pool

    @staticmethod
    def conectar():
        
        #Pide una conexión del pool para usarla en los DAOs.
        pool = MySQLConnection.get_pool()
        if not pool:
            return None
        
        try:
            conn = pool.get_connection()
            if conn.is_connected():
                return conn
            return None
        except Exception as e:
            print(f"Error al conectar a MySQL: {e}")
            return None