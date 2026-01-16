from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.daos.usuario_dao import UsuarioDAO

router = APIRouter()

# Modelos para recibir los datos del JSON (Frontend)
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    nombre_completo: str
    username: str
    password: str

# --- LOGIN ---
@router.post("/api/login")
async def login(datos: LoginRequest):
    usuario = UsuarioDAO.verificar_credenciales(datos.username, datos.password)
    
    if usuario:
        return {
            "mensaje": "Login exitoso", 
            "usuario": usuario['nombre_completo'], 
            "rol": usuario['rol']
        }
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# --- REGISTRO ---
@router.post("/api/register")
async def register(datos: RegisterRequest):
    exito = UsuarioDAO.crear_usuario(datos.nombre_completo, datos.username, datos.password)
    
    if exito:
        return {"mensaje": "Usuario creado correctamente"}
    else:
        # Probablemente el usuario ya existe
        raise HTTPException(status_code=400, detail="Error al crear usuario (quizás el usuario ya existe)")