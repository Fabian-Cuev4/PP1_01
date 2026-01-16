# Este archivo maneja la seguridad: el inicio de sesión (Login) y la creación de cuentas (Registro).

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.daos.usuario_dao import UsuarioDAO

# Creamos el router para las rutas de autenticación
router = APIRouter()

# Modelos de datos
# Definimos qué datos esperamos recibir del formulario de la web (JS)
class LoginRequest(BaseModel):
    username: str # El nombre de usuario que escribe el cliente
    password: str # La contraseña

class RegisterRequest(BaseModel):
    nombre_completo: str # Nombre real de la persona
    username: str        # Nombre de usuario único
    password: str        # Su clave

# Ruta para iniciar sesión (Login)
@router.post("/api/login")
async def login(datos: LoginRequest):
    """
    Recibe el usuario y clave del frontend y pregunta a la base de datos si son correctos.
    """
    # Buscamos en la base de datos usando el DAO (Data Access Object)
    usuario = UsuarioDAO.verificar_credenciales(datos.username, datos.password)
    
    if usuario:
        # Si lo encuentra, enviamos un mensaje de éxito con sus datos
        return {
            "mensaje": "Login exitoso", 
            "usuario": usuario['nombre_completo'], 
            "rol": usuario['rol']
        }
    else:
        # Si NO lo encuentra, enviamos un error 401 (No autorizado)
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# ruta para registrar un nuevo usuario
@router.post("/api/register")
async def register(datos: RegisterRequest):
    """
    Recibe los datos del nuevo usuario y los guarda en MySQL.
    """
    # Intentamos crear el usuario en la base de datos
    exito = UsuarioDAO.crear_usuario(datos.nombre_completo, datos.username, datos.password)
    
    if exito:
        # Si se guardó bien
        return {"mensaje": "Usuario creado correctamente"}
    else:
        # Si falló (por ejemplo, si el nombre de usuario ya está ocupado)
        raise HTTPException(status_code=400, detail="Error al crear usuario (quizás el usuario ya existe)")