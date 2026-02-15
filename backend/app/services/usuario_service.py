# SERVICE LIMPIO - Solo lógica de negocio, sin acceso a datos
# Responsabilidades: validación de negocio, coordinación con DAOs

from app.daos.usuario_dao import UsuarioDAO
from app.models.Usuario import Usuario

class UsuarioService:
    def __init__(self):
        self.dao = UsuarioDAO()
    
    def registrar_usuario(self, datos: dict) -> tuple:
        # Registra un nuevo usuario con validaciones de negocio
        try:
            # Validaciones de negocio
            if not all([datos.get('nombre_completo'), datos.get('username'), datos.get('password')]):
                return None, "Todos los campos son requeridos"
            
            if len(datos.get('password', '')) < 6:
                return None, "La contraseña debe tener al menos 6 caracteres"
            
            # Verificar si el usuario ya existe
            if self.dao.obtener_usuario_por_username(datos.get('username')):
                return None, "El nombre de usuario ya existe"
            
            # Crear objeto usuario con rol por defecto
            usuario = Usuario(
                datos.get('nombre_completo'),
                datos.get('username'),
                datos.get('password'),
                datos.get('rol', 'usuario')
            )
            
            # Guardar usuario
            if self.dao.guardar(usuario):
                return {"mensaje": "Usuario creado correctamente"}, None
            
            return None, "Error al crear usuario"
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error en el servicio: {str(e)}"
    
    def autenticar_usuario(self, username: str, password: str) -> tuple:
        # Autentica un usuario y maneja la sesión
        try:
            if not username or not password:
                return None, "Usuario y contraseña son requeridos"
            
            # Verificar credenciales
            usuario = self.dao.verificar_credenciales(username, password)
            
            if usuario:
                return {
                    "mensaje": "Login exitoso",
                    "token": username,  # Token temporal
                    "usuario": {
                        "nombre_completo": usuario['nombre_completo'],
                        "username": usuario['username'],
                        "rol": usuario['rol']
                    }
                }, None
            
            return None, "Usuario o contraseña incorrectos"
            
        except Exception as e:
            return None, f"Error en el servicio: {str(e)}"
    
    def obtener_usuario(self, username: str) -> tuple:
        # Obtiene datos de un usuario
        try:
            usuario = self.dao.obtener_usuario_por_username(username)
            if usuario:
                # Eliminar contraseña del resultado
                if 'password' in usuario:
                    del usuario['password']
                return usuario, None
            return None, "Usuario no encontrado"
        except Exception as e:
            return None, f"Error en el servicio: {str(e)}"
    
    def obtener_usuarios_activos(self) -> tuple:
        # Obtiene lista de usuarios activos (sin Redis - devuelve lista vacía)
        try:
            return [], None
        except Exception as e:
            return [], f"Error al obtener usuarios activos: {str(e)}"
    
    def cerrar_sesion(self, username: str) -> tuple:
        # Cierra la sesión de un usuario (sin Redis - solo confirma)
        try:
            return {"mensaje": "Sesión cerrada correctamente"}, None
        except Exception as e:
            return None, f"Error al cerrar sesión: {str(e)}"
