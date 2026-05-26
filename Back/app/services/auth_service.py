from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import resend

from app.repositories import auth_repository
from app.models.models import UsuarioLogin, UsuarioRegistro
from app.core.security import decodificar_token
import resend

#tengo que crear una cuenta en resend y generar una API key para enviar correos de bienvenida a los usuarios registrados.

resend.api_key = "re_QTZTpctm_KdGBHgDP9B27wkWih6PGDiU3"

security = HTTPBearer()

async def login_usuario(datos: UsuarioLogin) -> dict:
    return await auth_repository.obtener_usuario(datos)

async def registro_usuario(datos: UsuarioRegistro) -> dict:
    resultado= await auth_repository.crear_usuario(datos)
    
    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": "nabiliomg345@gmail.com",
        "subject": "Bienvenido a CVBoost",
        "html": "<p>¡Hola! Gracias por registrarte en CVBoost.</p>"
    })
    return resultado

async def actualizar_perfil_usuario(datos: dict, current_user: dict) -> dict:
    return await auth_repository.actualizar_usuario(datos, current_user)

async def cambiar_contraseña(datos: dict, current_user: dict) -> dict:
    return await auth_repository.cambiar_contraseña(datos, current_user)

async def obtener_perfil_usuario(current_user: dict) -> dict:
    return await auth_repository.obtener_perfil_usuario(current_user)

async def eliminar_cuenta(current_user: dict) -> dict:
    return await auth_repository.eliminar_usuario(current_user)

async def cerrar_sesion(current_user: dict) -> dict:
    return {"mensaje": "Sesión cerrada correctamente"}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return payload  # contiene {"id_usuario": ..., "email": ...}
