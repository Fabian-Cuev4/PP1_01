from pydantic import BaseModel

# DTO (Data Transfer Object) para usuario
# Sirve para estandarizar la transferencia de datos de usuario
class UsuarioDTO(BaseModel):
    id: int                    # ID del usuario en la base de datos
    nombre_completo: str        # Nombre completo del usuario
    username: str              # Nombre de usuario único
    rol: str                   # Rol del usuario (admin, usuario)
    fecha_registro: str         # Fecha de registro
    
    class Config:
        from_attributes = True  # Permite crear desde objetos con atributos
