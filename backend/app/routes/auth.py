# Este archivo maneja la autenticación: login y registro de usuarios
# Las rutas son las direcciones que el frontend usa para comunicarse con el backend

# Importamos las librerías necesarias
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.daos.usuario_dao import UsuarioDAO

# Creamos un router para agrupar todas las rutas de autenticación
router = APIRouter()

# Creamos instancia directa del DAO
usuario_dao = UsuarioDAO()

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
    # Validamos datos de entrada
    if not datos.username or not datos.password:
        raise HTTPException(status_code=400, detail="Usuario y contraseña son requeridos")
    
    # Llamamos directamente al DAO para verificar credenciales
    usuario = usuario_dao.verificar_credenciales(datos.username, datos.password)
    
    if usuario:
        return {
            "mensaje": "Login exitoso", 
            "usuario": usuario['nombre_completo'], 
            "username": usuario['username'],
            "rol": usuario['rol']
        }
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# Esta ruta se ejecuta cuando el frontend hace POST a /api/register
@router.post("/api/register")
async def register(datos: RegisterRequest):
    # Validamos datos de entrada
    if not all([datos.nombre_completo, datos.username, datos.password]):
        raise HTTPException(status_code=400, detail="Todos los campos son requeridos")
    
    if len(datos.password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
    
    # Llamamos directamente al DAO para crear el usuario
    exito = usuario_dao.crear_usuario(datos.nombre_completo, datos.username, datos.password)
    
    if exito:
        return {"mensaje": "Usuario creado correctamente"}
    else:
        raise HTTPException(status_code=400, detail="Error al crear usuario (quizás el usuario ya existe)")
