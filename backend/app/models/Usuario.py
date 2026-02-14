from app.models.abstrac_factory.Persona import Persona

# Representa un usuario del sistema
class Usuario(Persona):
    def __init__(self, nombre_completo, username, password, rol="usuario", fecha_registro=None):
        super().__init__(nombre_completo, "Usuario", fecha_registro)
        self.username = username
        self.password = password  # En producción debería estar hasheada
        self.rol = rol  # admin, usuario, etc.
    
    def obtener_tipo_especifico(self):
        # Retorna el tipo específico de usuario
        return "USER"
    
    def validar_datos(self):
        # Valida datos específicos de usuario
        if not self.nombre_completo or not self.nombre_completo.strip():
            raise ValueError("El nombre completo es requerido")
        if not self.username or not self.username.strip():
            raise ValueError("El nombre de usuario es requerido")
        if len(self.username) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        if not self.password or len(self.password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        if self.rol not in ["admin", "usuario"]:
            raise ValueError("El rol debe ser 'admin' o 'usuario'")
        return True
    
    def to_dict(self):
        # Convierte el usuario a diccionario para guardar en BD
        return {
            "nombre_completo": self.nombre_completo,
            "tipo_persona": self.tipo_persona,
            "username": self.username,
            "password": self.password,  # El DAO se encargará del hasheo
            "rol": self.rol
        }
