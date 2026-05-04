from datetime import datetime

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import create_engine
from io import BytesIO
import os
import traceback

from fastapi import FastAPI, HTTPException
# from fastapi.datastructures import FormData
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

from app.models import FormDataModel, Usuario, UsuarioLogin
from app.routers.auth import crear_token, decodificar_token, hashear_password, verificar_password

router = APIRouter()
security = HTTPBearer()



# conectar MYSQL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:abc123.@localhost:3306/cv_generator")
engine = create_engine(DATABASE_URL)

# ── dependencia reutilizable para rutas protegidas ──────────────────
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return payload  # contiene {"id_usuario": ..., "email": ..

# ── REGISTRO ────────────────────────────────────────────────────────
@router.post("/registro")
async def registrar_usuario(usuario: Usuario):
    try:
        with engine.begin() as connection:
            result = connection.execute(
                text("SELECT id_usuario FROM USUARIO WHERE email = :email"),
                {"email": usuario.email}
            )
            if result.fetchone():
                raise HTTPException(status_code=400, detail="El correo ya está registrado")

            connection.execute(
                text("""
                    INSERT INTO USUARIO (nombre, apellidos, email, contrasena, fecha_creacion)
                    VALUES (:nombre, :apellidos, :email, :contrasena, :fecha_creacion)
                """),
                {
                    "nombre": usuario.nombre,
                    "apellidos": usuario.apellidos,
                    "email": usuario.email,
                    "contrasena": hashear_password(usuario.contrasena),  # ← hasheada
                    "fecha_creacion": datetime.now()
                }
            )
        return {"message": "Usuario registrado exitosamente"}
    except HTTPException:
        raise
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al registrar el usuario")


# ── LOGIN ────────────────────────────────────────────────────────────

@router.post("/login")
async def login(datos: UsuarioLogin):
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT id_usuario, nombre, contrasena FROM USUARIO WHERE email = :email"),
                {"email": datos.email}
            )
            usuario = result.fetchone()

            if not usuario or not verificar_password(datos.contrasena, usuario.contrasena):
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

            token = crear_token({"id_usuario": usuario.id_usuario, "email": datos.email})
            return {
                "access_token": token,
                "token_type": "bearer",
                "nombre": usuario.nombre  # ← aquí
            }
    except HTTPException:
        raise
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al iniciar sesión")


# ── EJEMPLO RUTA PROTEGIDA ───────────────────────────────────────────
@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"id_usuario": current_user["id_usuario"], "email": current_user["email"]}