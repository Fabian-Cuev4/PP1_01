# SERVICE LIMPIO - Solo lógica de negocio, integrado con Redis para sesiones
# Responsabilidades: validación de negocio, coordinación con DAOs y caché de sesiones

from app.daos.usuario_dao import UsuarioDAO
from app.models.Usuario import Usuario
from app.database.redis_client import RedisClient
import json

class UsuarioService:
    def __init__(self):
        self.dao = UsuarioDAO()
        # --- Cliente Redis original ---
        self._redis = RedisClient.get_client()
        self._session_ttl = 3600  # 1 hora de sesión

    def registrar_usuario(self, datos: dict) -> tuple:
        try:
            if not all([datos.get('nombre_completo'), datos.get('username'), datos.get('password')]):
                return None, "Todos los campos son requeridos"
            
            if len(datos.get('password', '')) < 6:
                return None, "La contraseña debe tener al menos 6 caracteres"
            
            if self.dao.obtener_usuario_por_username(datos.get('username')):
                return None, "El nombre de usuario ya existe"
            
            usuario = Usuario(
                datos.get('nombre_completo'),
                datos.get('username'),
                datos.get('password'),
                datos.get('rol', 'usuario')
            )
            
            if self.dao.guardar(usuario):
                # Invalidad caché de lista de usuarios si existiera
                self._redis.delete("usuarios:all")
                return {"mensaje": "Usuario creado correctamente"}, None
            
            return None, "Error al crear usuario"
            
        except Exception as e:
            return None, f"Error en el servicio: {str(e)}"
    
    def autenticar_usuario(self, username: str, password: str) -> tuple:
        try:
            if not username or not password:
                return None, "Usuario y contraseña son requeridos"
            
            usuario = self.dao.verificar_credenciales(username, password)
            
            if usuario:
                user_data = {
                    "nombre_completo": usuario['nombre_completo'],
                    "username": usuario['username'],
                    "rol": usuario['rol']
                }
                
                # 🔥 LÓGICA REDIS: Guardar sesión activa (Tu implementación)
                # Usamos un set para usuarios activos y una llave para el perfil
                self._redis.sadd("usuarios:activos", username)
                self._redis.setex(
                    f"sesion:{username}", 
                    self._session_ttl, 
                    json.dumps(user_data)
                )

                return {
                    "mensaje": "Login exitoso",
                    "token": f"session_token_{username}", 
                    "usuario": user_data
                }, None
            
            return None, "Usuario o contraseña incorrectos"
            
        except Exception as e:
            return None, f"Error en el servicio: {str(e)}"
    
    def obtener_usuarios_activos(self) -> tuple:
        # 🔥 LÓGICA REDIS: Recuperar desde el set de sesiones
        try:
            activos = self._redis.smembers("usuarios:activos")
            # Convertir de bytes a string
            lista_activos = [u.decode('utf-8') if isinstance(u, bytes) else u for u in activos]
            return lista_activos, None
        except Exception as e:
            return [], f"Error al obtener usuarios activos de Redis: {str(e)}"
    
    def cerrar_sesion(self, username: str) -> tuple:
        # 🔥 LÓGICA REDIS: Limpiar sesión
        try:
            self._redis.srem("usuarios:activos", username)
            self._redis.delete(f"sesion:{username}")
            return {"mensaje": "Sesión cerrada correctamente"}, None
        except Exception as e:
            return None, f"Error al cerrar sesión: {str(e)}"

    def obtener_usuario(self, username: str) -> tuple:
        try:
            usuario = self.dao.obtener_usuario_por_username(username)
            if usuario:
                if 'password' in usuario:
                    del usuario['password']
                return usuario, None
            return None, "Usuario no encontrado"
        except Exception as e:
            return None, f"Error en el servicio: {str(e)}"