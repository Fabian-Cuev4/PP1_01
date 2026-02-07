# Lógica de negocio de usuarios
# Service es el cerebro: valida y prepara los datos

# Importamos clases necesarias
from app.daos.usuario_dao import UsuarioDAO
from app.utils.encryption import Encryption

class UsuarioService:
    # Coordina todas las operaciones de usuarios
    
    def __init__(self, usuario_dao):
        # Guardamos referencia al DAO para uso posterior
        self._usuario_dao = usuario_dao
    
    def registrar_usuario(self, nombre_completo, username, password):
        # Crea nuevo usuario con todas las validaciones
        
        # Validación: nombre completo no puede estar vacío
        if not nombre_completo or nombre_completo.strip() == "":
            return False, "El nombre completo es obligatorio"
        
        # Validación: username no puede estar vacío
        if not username or username.strip() == "":
            return False, "El nombre de usuario es obligatorio"
        
        # Validación: contraseña debe tener al menos 8 caracteres
        if not password or len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        # Validación: username debe ser único
        usuario_existente = self._usuario_dao.obtener_usuario_por_username(username)
        if usuario_existente:
            return False, "El nombre de usuario ya está en uso"
        
        # Encriptamos contraseña
        password_encriptado = Encryption.encriptar_password(password)
        
        # Llamamos al DAO para guardar usuario en base de datos
        exito = self._usuario_dao.crear_usuario(nombre_completo, username, password_encriptado)
        
        if exito:
            return True, "Usuario creado correctamente"
        else:
            return False, "Error al crear el usuario en la base de datos"
    
    def login_usuario(self, username, password):
        # Verifica credenciales del usuario
        
        # Validación básica
        if not username or not password:
            return None, "Usuario y contraseña son obligatorios"
        
        # Obtenemos usuario de base de datos
        usuario = self._usuario_dao.obtener_usuario_por_username(username)
        
        # Si no encontramos usuario, retornamos error
        if not usuario:
            return None, "Usuario o contraseña incorrectos"
        
        # Verificamos contraseña usando clase Encryption
        if Encryption.verificar_password(password, usuario['password']):
            # Contraseña correcta: retornamos datos sin contraseña
            usuario_seguro = {
                'id': usuario.get('id'),
                'nombre_completo': usuario.get('nombre_completo'),
                'username': usuario.get('username'),
                'rol': usuario.get('rol', 'usuario')
            }
            return usuario_seguro, "Login exitoso"
        else:
            return None, "Usuario o contraseña incorrectos"
    
    def obtener_usuario(self, username):
        # Obtiene datos de usuario por su username
        
        # Validación básica
        if not username:
            return None, "El nombre de usuario es obligatorio"
        
        # Obtenemos usuario de base de datos
        usuario = self._usuario_dao.obtener_usuario_por_username(username)
        
        if usuario:
            # Quitamos contraseña por seguridad
            usuario_seguro = {
                'id': usuario.get('id'),
                'nombre_completo': usuario.get('nombre_completo'),
                'username': usuario.get('username'),
                'rol': usuario.get('rol', 'usuario')
            }
            return usuario_seguro, None
        else:
            return None, "Usuario no encontrado"
