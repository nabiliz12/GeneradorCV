from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services import auth_service
from app.models.models import UsuarioLogin, UsuarioRegistro
from app.services.auth_service import get_current_user


# AQUI SOLO LOS ENDPOINTS

security = HTTPBearer()
app = APIRouter()

@app.post("/login")
async def login(datos: UsuarioLogin):
    return await auth_service.login_usuario(datos)

@app.post("/registro")
async def registrar_usuario(datos: UsuarioRegistro):
    return await auth_service.registro_usuario(datos)

@app.put("/actualizar_perfil")
async def actualizar_perfil_usuario(datos: dict, current_user: dict = Depends(get_current_user)):
    return await auth_service.actualizar_perfil_usuario(datos, current_user)

@app.put("/cambiar_contraseña")
async def cambiar_contraseña(datos: dict, current_user: dict = Depends(get_current_user)):
    return await auth_service.cambiar_contraseña(datos, current_user)

@app.get("/perfil")
async def obtener_perfil_usuario(current_user: dict = Depends(get_current_user)):
    return await auth_service.obtener_perfil_usuario(current_user)
    
@app.delete("/usuario")
async def eliminar_cuenta(current_user: dict = Depends(get_current_user)):
    return await auth_service.eliminar_cuenta(current_user)

@app.post("/cerrar_sesion")
async def cerrar_sesion(current_user: dict = Depends(get_current_user)):
    return await auth_service.cerrar_sesion(current_user)


