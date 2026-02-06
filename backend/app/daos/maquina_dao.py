# Este archivo se encarga de guardar y buscar máquinas en la base de datos MySQL
# DAO significa "Data Access Object" (Objeto de Acceso a Datos)
# Su única función es ejecutar SQL puro, sin lógica de negocio

# Importamos la clase que maneja la conexión a MySQL
from app.database.mysql import MySQLConnection

class MaquinaDAO:
    # Esta función guarda una máquina nueva en la base de datos
    # Recibe un objeto máquina con todos los datos listos para guardar
    def guardar(self, maquina):
        # Obtenemos una conexión a la base de datos
        conn = MySQLConnection.conectar()
        # Si no hay conexión, salimos de la función
        if not conn:
            return False
        
        try:
            # Creamos un cursor para ejecutar comandos SQL
            cursor = conn.cursor()
            # Definimos la consulta SQL para insertar una máquina
            query = """
                INSERT INTO maquinas (codigo, tipo, estado, area, fecha, usuario) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            # Ejecutamos la consulta pasándole los valores de la máquina
            cursor.execute(query, (
                maquina.codigo_equipo, 
                maquina.tipo_equipo, 
                maquina.estado_actual, 
                maquina.area, 
                maquina.fecha,
                maquina.usuario
            ))
            # Confirmamos los cambios (commit)
            conn.commit()
            # Cerramos el cursor y la conexión
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos False
            print(f"Error al guardar máquina: {e}")
            return False

    # Esta función actualiza los datos de una máquina existente
    # Recibe un objeto máquina con los datos actualizados
    def actualizar(self, maquina):
        # Obtenemos una conexión a la base de datos
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            # Creamos un cursor para ejecutar comandos SQL
            cursor = conn.cursor()
            # Definimos la consulta SQL para actualizar una máquina
            query = """
                UPDATE maquinas 
                SET tipo = %s, estado = %s, area = %s, fecha = %s, usuario = %s
                WHERE codigo = %s
            """
            # Ejecutamos la consulta pasándole los nuevos valores
            cursor.execute(query, (
                maquina.tipo_equipo,
                maquina.estado_actual,
                maquina.area,
                maquina.fecha,
                maquina.usuario,
                maquina.codigo_equipo
            ))
            # Confirmamos los cambios
            conn.commit()
            # Cerramos el cursor y la conexión
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos False
            print(f"Error al actualizar máquina: {e}")
            return False

    # Esta función elimina una máquina de la base de datos
    # Recibe el código de la máquina a eliminar
    def eliminar(self, codigo):
        # Obtenemos una conexión a la base de datos
        conn = MySQLConnection.conectar()
        if not conn:
            return False
        
        try:
            # Creamos un cursor para ejecutar comandos SQL
            cursor = conn.cursor()
            # Definimos la consulta SQL para eliminar una máquina
            query = "DELETE FROM maquinas WHERE codigo = %s"
            # Ejecutamos la consulta pasándole el código
            cursor.execute(query, (codigo,))
            # Confirmamos los cambios
            conn.commit()
            # Cerramos el cursor y la conexión
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos False
            print(f"Error al eliminar máquina: {e}")
            return False

    # Esta función busca una máquina por su código
    # Recibe el código a buscar y retorna los datos de la máquina
    def buscar_por_codigo(self, codigo):
        # Obtenemos una conexión a la base de datos
        conn = MySQLConnection.conectar()
        if not conn:
            return None
        
        try:
            # Creamos un cursor que retorna diccionarios (más fácil de usar)
            cursor = conn.cursor(dictionary=True)
            # Definimos la consulta SQL para buscar una máquina
            # Usamos LOWER para que la búsqueda no sea sensible a mayúsculas/minúsculas
            query = "SELECT * FROM maquinas WHERE LOWER(codigo) = LOWER(%s)"
            # Ejecutamos la consulta pasándole el código
            cursor.execute(query, (codigo.strip().lower(),))
            # Obtenemos el primer resultado (si existe)
            resultado = cursor.fetchone()
            # Cerramos el cursor y la conexión
            cursor.close()
            conn.close()
            return resultado
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos None
            print(f"Error al buscar máquina: {e}")
            return None

    # Esta función obtiene todas las máquinas de la base de datos
    # Retorna una lista con todas las máquinas
    def listar_todas(self):
        # Obtenemos una conexión a la base de datos
        conn = MySQLConnection.conectar()
        if not conn:
            return []
        
        try:
            # Creamos un cursor que retorna diccionarios
            cursor = conn.cursor(dictionary=True)
            # Ejecutamos la consulta para obtener todas las máquinas
            cursor.execute("SELECT * FROM maquinas")
            # Obtenemos todos los resultados
            lista = cursor.fetchall()
            # Cerramos el cursor y la conexión
            cursor.close()
            conn.close()
            return lista
        except Exception as e:
            # Si hay un error, lo imprimimos y retornamos una lista vacía
            print(f"Error al listar máquinas: {e}")
            return []
