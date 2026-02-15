# ROUTES LIMPIAS - Solo validación HTTP y respuestas
# Responsabilidades: validación de entrada, respuestas HTTP, coordinación con services

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.usuario_service import UsuarioService

router = APIRouter()
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

@router.post("/api/login")
async def login(datos: LoginRequest):
    # Inicia sesión de usuario
    try:
        resultado, error = service.autenticar_usuario(datos.username, datos.password)
        if error:
            raise HTTPException(status_code=401, detail=error)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/register")
async def register(datos: RegisterRequest):
    # Registra un nuevo usuario
    try:
        resultado, error = service.registrar_usuario(datos.model_dump())
        if error:
            raise HTTPException(status_code=400, detail=error)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/usuarios/activos")
async def listar_usuarios_activos():
    # Obtiene lista de usuarios activos
    try:
        resultado, error = service.obtener_usuarios_activos()
        if error:
            raise HTTPException(status_code=500, detail=error)
        return {"usuarios_activos": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/logout")
async def logout(username: str):
    # Cierra sesión de usuario
    try:
        resultado, error = service.cerrar_sesion(username)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
