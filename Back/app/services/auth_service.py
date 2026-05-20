from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.repositories import auth_repository
from app.models.models import UsuarioLogin, UsuarioRegistro
from app.core.security import decodificar_token

security = HTTPBearer()


async def login_usuario(datos: UsuarioLogin) -> dict:
    return await auth_repository.obtener_usuario(datos)

async def registro_usuario(datos: UsuarioRegistro) -> dict:
    return await auth_repository.crear_usuario(datos)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return payload  # contiene {"id_usuario": ..., "email": ...}
