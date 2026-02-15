# ROUTES LIMPIAS - Solo validación HTTP y respuestas
# Responsabilidades: validación de entrada, respuestas HTTP, coordinación con services

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/api/auth")
service = UsuarioService()

# Modelos para validación de entrada
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    nombre_completo: str
    username: str
    password: str
    rol: str = "usuario"

@router.post("/login")
async def login(datos: LoginRequest):
    # Inicia sesión de usuario
    try:
        resultado, error = service.autenticar_usuario(datos.username, datos.password)
        if error:
            raise HTTPException(status_code=401, detail=error)
        return resultado
    except HTTPException:
        # Dejar pasar las excepciones HTTP (como 401)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register(datos: RegisterRequest):
    # Registra un nuevo usuario
    try:
        resultado, error = service.registrar_usuario(datos.model_dump())
        if error:
            raise HTTPException(status_code=400, detail=error)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

