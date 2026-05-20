from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services import auth_service
from app.models.models import UsuarioLogin, UsuarioRegistro


# AQUI SOLO LOS ENDPOINTS

security = HTTPBearer()
app = APIRouter()

@app.post("/login")
async def login(datos: UsuarioLogin):
    return await auth_service.login_usuario(datos)
    
@app.post("/registro")
async def registrar_usuario(datos: UsuarioRegistro):
    return await auth_service.registro_usuario(datos)

# ── dependencia reutilizable para rutas protegidas ──────────────────
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return auth_service.get_current_user(credentials)
