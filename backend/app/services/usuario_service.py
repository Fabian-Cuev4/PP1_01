# Service - Lógica de negocio de usuarios
# Responsabilidades: validación de negocio, coordinación con DAOs

from app.daos.usuario_dao import UsuarioDAO
from app.models.Usuario import Usuario

class UsuarioService:
    def __init__(self):
        self.dao = UsuarioDAO()
    
    def registrar_usuario(self, datos: dict) -> tuple:
        # Registra nuevo usuario con validaciones
        try:
            print(f"DEBUG: Datos recibidos: {datos}")
            
            # Validaciones de negocio
            if not all([datos.get('nombre_completo'), datos.get('username'), datos.get('password')]):
                print("DEBUG: Faltan campos requeridos")
                return None, "Todos los campos son requeridos"
            
            if len(datos.get('password', '')) < 6:
                print("DEBUG: Contraseña muy corta")
                return None, "La contraseña debe tener al menos 6 caracteres"
            
            # Verificar si usuario ya existe
            usuario_existente = self.dao.obtener_usuario_por_username(datos.get('username'))
            print(f"DEBUG: Usuario existente: {usuario_existente}")
            if usuario_existente:
                return None, "El nombre de usuario ya existe"
            
            # Crear objeto usuario con rol por defecto
            usuario = Usuario(
                datos.get('nombre_completo'),
                datos.get('username'),
                datos.get('password'),
                datos.get('rol', 'usuario')
            )
            
            print(f"DEBUG: Usuario creado: {usuario.to_dict()}")
            
            # Validar datos del modelo
            try:
                usuario.validar_datos()
                print("DEBUG: Validación exitosa")
            except ValueError as e:
                print(f"DEBUG: Error en validación: {e}")
                return None, str(e)
            
            # Guardar usuario
            resultado = self.dao.guardar(usuario)
            print(f"DEBUG: Resultado guardado: {resultado}")
            
            if resultado:
                return {"mensaje": "Usuario creado correctamente"}, None
            
            return None, "Error al crear usuario"
            
        except ValueError as e:
            print(f"DEBUG: ValueError: {e}")
            return None, str(e)
        except Exception as e:
            print(f"DEBUG: Exception general: {e}")
            return None, f"Error en el servicio: {str(e)}"
    
    def autenticar_usuario(self, username: str, password: str) -> tuple:
        # Autentica usuario y maneja sesión
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
        # Obtiene datos de usuario
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
        # Cierra sesión de usuario (sin Redis - solo confirma)
        try:
            return {"mensaje": "Sesión cerrada correctamente"}, None
        except Exception as e:
            return None, f"Error al cerrar sesión: {str(e)}"
