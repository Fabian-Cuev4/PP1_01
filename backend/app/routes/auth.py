# Este archivo maneja la autenticación: login y registro de usuarios
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend
# Router solo llama al Service, no conoce la base de datos ni cómo se encripta

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.usuario_service import UsuarioService
from app.repositories.proyecto_repository import get_repository

# Creamos un router para agrupar todas las rutas de autenticación
router = APIRouter()

# Obtenemos la instancia del repository y creamos el service
repository = get_repository()
usuario_service = UsuarioService(repository.get_usuario_dao())

# Definimos cómo deben ser los datos que recibimos del frontend para login
class LoginRequest(BaseModel):
    username: str  # Nombre de usuario
    password: str  # Contraseña

# Definimos cómo deben ser los datos que recibimos del frontend para registro
class RegisterRequest(BaseModel):
    nombre_completo: str  # Nombre completo de la persona
    username: str         # Nombre de usuario único
    password: str         # Contraseña

# Esta ruta se ejecuta cuando el frontend hace POST a /api/login
@router.post("/api/login")
async def login(datos: LoginRequest):
    # Llamamos al Service para verificar las credenciales
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
        # Si no encontramos el usuario, retornamos un error HTTP 401 (No autorizado)
        raise HTTPException(status_code=401, detail=mensaje)

# Esta ruta se ejecuta cuando el frontend hace POST a /api/register
@router.post("/api/register")
async def register(datos: RegisterRequest):
    # Llamamos al Service para crear el nuevo usuario con validaciones
    exito, mensaje = usuario_service.registrar_usuario(datos.nombre_completo, datos.username, datos.password)
    
    # Si se creó correctamente, retornamos un mensaje de éxito
    if exito:
        return {"mensaje": mensaje}
    else:
        # Si falló (por ejemplo, el usuario ya existe), retornamos un error HTTP 400
        raise HTTPException(status_code=400, detail=mensaje)
