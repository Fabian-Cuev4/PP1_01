# Este archivo maneja la autenticación: login y registro de usuarios
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.daos.usuario_dao import UsuarioDAO

# Creamos un router para agrupar todas las rutas de autenticación
router = APIRouter()

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
    # Llamamos al DAO para verificar si el usuario y contraseña son correctos
    usuario = UsuarioDAO.verificar_credenciales(datos.username, datos.password)
    
    # Si encontramos el usuario, retornamos sus datos
    if usuario:
        return {
            "mensaje": "Login exitoso", 
            "usuario": usuario['nombre_completo'], 
            "username": usuario['username'],
            "rol": usuario['rol']
        }
    else:
        # Si no encontramos el usuario, retornamos un error HTTP 401 (No autorizado)
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# Esta ruta se ejecuta cuando el frontend hace POST a /api/register
@router.post("/api/register")
async def register(datos: RegisterRequest):
    # Llamamos al DAO para crear el nuevo usuario
    exito = UsuarioDAO.crear_usuario(datos.nombre_completo, datos.username, datos.password)
    
    # Si se creó correctamente, retornamos un mensaje de éxito
    if exito:
        return {"mensaje": "Usuario creado correctamente"}
    else:
        # Si falló (por ejemplo, el usuario ya existe), retornamos un error HTTP 400
        raise HTTPException(status_code=400, detail="Error al crear usuario (quizás el usuario ya existe)")
