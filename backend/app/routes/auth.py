# Manejo de autenticación: login y registro de usuarios
# Router llama al Service, no conoce la base de datos ni encriptación

# Importamos librerías necesarias
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.usuario_service import UsuarioService
from app.repositories.proyecto_repository import get_repository

# Router para agrupar rutas de autenticación
router = APIRouter()

# Obtenemos repository y creamos servicio
repository = get_repository()
usuario_service = UsuarioService(repository.get_usuario_dao())

# Schema para datos de login desde frontend
class LoginRequest(BaseModel):
    username: str  # Nombre de usuario
    password: str  # Contraseña

# Schema para datos de registro desde frontend
class RegisterRequest(BaseModel):
    nombre_completo: str  # Nombre completo de la persona
    username: str         # Nombre de usuario único
    password: str         # Contraseña

# Endpoint para login de usuarios
@router.post("/api/login")
async def login(datos: LoginRequest):
    # Llamamos al Service para verificar credenciales
    usuario, mensaje = usuario_service.login_usuario(datos.username, datos.password)
    
    # Si encontramos el usuario, retornamos sus datos
    if usuario:
        return {
            "mensaje": mensaje, 
            "usuario": usuario['nombre_completo'], 
            "username": usuario['username'],
            "rol": usuario.get('rol', 'usuario')
        }
    else:
        # Si no encontramos el usuario, retornamos HTTP 401
        raise HTTPException(status_code=401, detail=mensaje)

# Endpoint para registro de nuevos usuarios
@router.post("/api/register")
async def register(datos: RegisterRequest):
    # Llamamos al Service para crear nuevo usuario con validaciones
    exito, mensaje = usuario_service.registrar_usuario(datos.nombre_completo, datos.username, datos.password)
    
    # Si se creó correctamente, retornamos mensaje de éxito
    if exito:
        return {"mensaje": mensaje}
    else:
        # Si falló (usuario ya existe), retornamos HTTP 400
        raise HTTPException(status_code=400, detail=mensaje)
