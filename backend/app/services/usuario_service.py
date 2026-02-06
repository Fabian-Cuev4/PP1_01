# Este archivo se encarga de la lógica de negocio de usuarios
# Service es el cerebro: aquí validamos y preparamos los datos

# Importamos las clases necesarias
from app.daos.usuario_dao import UsuarioDAO
from app.utils.encryption import Encryption

class UsuarioService:
    # Esta clase coordina todas las operaciones de usuarios
    
    def __init__(self, usuario_dao):
        # Guardamos la referencia al DAO para usarla después
        self._usuario_dao = usuario_dao
    
    def registrar_usuario(self, nombre_completo, username, password):
        # Esta función crea un nuevo usuario con todas las validaciones
        
        # Validación: el nombre completo no puede estar vacío
        if not nombre_completo or nombre_completo.strip() == "":
            return False, "El nombre completo es obligatorio"
        
        # Validación: el username no puede estar vacío
        if not username or username.strip() == "":
            return False, "El nombre de usuario es obligatorio"
        
        # Validación: la contraseña debe tener al menos 8 caracteres
        if not password or len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        # Validación: el username debe ser único
        usuario_existente = self._usuario_dao.obtener_usuario_por_username(username)
        if usuario_existente:
            return False, "El nombre de usuario ya está en uso"
        
        # Si todas las validaciones pasan, encriptamos la contraseña
        password_encriptado = Encryption.encriptar_password(password)
        
        # Llamamos al DAO para guardar el usuario en la base de datos
        exito = self._usuario_dao.crear_usuario(nombre_completo, username, password_encriptado)
        
        if exito:
            return True, "Usuario creado correctamente"
        else:
            return False, "Error al crear el usuario en la base de datos"
    
    def login_usuario(self, username, password):
        # Esta función verifica las credenciales del usuario
        
        # Validación básica
        if not username or not password:
            return None, "Usuario y contraseña son obligatorios"
        
        # Obtenemos el usuario de la base de datos
        usuario = self._usuario_dao.obtener_usuario_por_username(username)
        
        # Si no encontramos el usuario, retornamos error
        if not usuario:
            return None, "Usuario o contraseña incorrectos"
        
        # Verificamos la contraseña usando la clase Encryption
        if Encryption.verificar_password(password, usuario['password']):
            # Si la contraseña es correcta, retornamos los datos del usuario
            # Quitamos la contraseña del resultado por seguridad
            usuario_seguro = {
                'id': usuario.get('id'),
                'nombre_completo': usuario.get('nombre_completo'),
                'username': usuario.get('username'),
                'rol': usuario.get('rol', 'usuario')  # Rol por defecto si no tiene
            }
            return usuario_seguro, "Login exitoso"
        else:
            # Si la contraseña es incorrecta
            return None, "Usuario o contraseña incorrectos"
    
    def obtener_usuario(self, username):
        # Esta función obtiene los datos de un usuario por su username
        
        # Validación básica
        if not username:
            return None, "El nombre de usuario es obligatorio"
        
        # Obtenemos el usuario de la base de datos
        usuario = self._usuario_dao.obtener_usuario_por_username(username)
        
        if usuario:
            # Quitamos la contraseña del resultado por seguridad
            usuario_seguro = {
                'id': usuario.get('id'),
                'nombre_completo': usuario.get('nombre_completo'),
                'username': usuario.get('username'),
                'rol': usuario.get('rol', 'usuario')
            }
            return usuario_seguro, None
        else:
            return None, "Usuario no encontrado"
