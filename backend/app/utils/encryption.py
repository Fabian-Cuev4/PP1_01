# Funciones para encriptar y verificar contraseñas
# Usamos bcrypt - librería segura para encriptación de contraseñas

# Importamos librería bcrypt
import bcrypt

class Encryption:
    # Contiene métodos estáticos para trabajar con contraseñas
    
    # Encripta una contraseña
    @staticmethod
    def encriptar_password(password):
        # Generamos sal aleatoria para encriptación más segura
        salt = bcrypt.gensalt()
        # Encriptamos contraseña usando sal
        # Convertimos contraseña a bytes, encriptamos, luego a string
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    # Verifica si contraseña coincide con hash guardado
    @staticmethod
    def verificar_password(password, hash_guardado):
        try:
            # Comparamos contraseña ingresada con hash guardado
            # Retorna True si coinciden, False si no
            return bcrypt.checkpw(password.encode('utf-8'), hash_guardado.encode('utf-8'))
        except:
            # Si hay error, retornamos False
            return False
