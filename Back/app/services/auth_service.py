from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.repositories import auth_repository
from app.models.models import UsuarioLogin, UsuarioRegistro
from app.core.security import *

security = HTTPBearer()

async def login_usuario(datos: UsuarioLogin) -> dict:
    return await auth_repository.obtener_usuario(datos)

async def registro_usuario(datos: UsuarioRegistro) -> dict:
    return await auth_repository.crear_usuario(datos)

async def actualizar_perfil_usuario(datos: dict, current_user: dict) -> dict:
    return await auth_repository.actualizar_usuario(datos, current_user)

async def cambiar_contraseña(datos: dict, current_user: dict) -> dict:
    return await auth_repository.cambiar_contraseña(datos, current_user)

async def obtener_perfil_usuario(current_user: dict) -> dict:
    return await auth_repository.obtener_perfil_usuario(current_user)

async def eliminar_cuenta(current_user: dict) -> dict:
    return await auth_repository.eliminar_usuario(current_user)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return payload  # contiene {"id_usuario": ..., "email": ...}
