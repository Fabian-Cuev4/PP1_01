# Este archivo contiene funciones para encriptar y verificar contraseñas
# Usamos bcrypt que es una librería segura para encriptar contraseñas

# Importamos la librería bcrypt
import bcrypt

class Encryption:
    # Esta clase contiene métodos estáticos para trabajar con contraseñas
    
    # Esta función encripta una contraseña
    @staticmethod
    def encriptar_password(password):
        # Generamos una "sal" (salt) que es un valor aleatorio para hacer la encriptación más segura
        salt = bcrypt.gensalt()
        # Encriptamos la contraseña usando la sal
        # Primero convertimos la contraseña a bytes, luego la encriptamos, y finalmente la convertimos a string
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    # Esta función verifica si una contraseña coincide con el hash guardado
    @staticmethod
    def verificar_password(password, hash_guardado):
        try:
            # Comparamos la contraseña ingresada con el hash guardado
            # Si coinciden, retorna True, si no, retorna False
            return bcrypt.checkpw(password.encode('utf-8'), hash_guardado.encode('utf-8'))
        except:
            # Si hay algún error, retornamos False
            return False
