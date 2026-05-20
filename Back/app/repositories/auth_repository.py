#AQUI VA LO QUE SE VA A PERSISITIR EN LA BASE DE DATOS (CRUD)
import traceback
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import text

from app.core.database import engine
from app.models.models import UsuarioLogin, UsuarioRegistro
from app.core import security

async def obtener_usuario(datos: UsuarioLogin)-> dict:
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT id_usuario, nombre, contrasena FROM USUARIO WHERE email = :email"),
                {"email": datos.email}
            )
            usuario = result.fetchone()

            if not usuario or not security.verificar_password(datos.contrasena, usuario.contrasena):
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

            token = security.crear_token({"id_usuario": usuario.id_usuario, "email": datos.email})
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
    

async def crear_usuario(usuario: UsuarioRegistro):
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
                    "contrasena": security.hashear_password(usuario.contrasena),  # ← hasheada
                    "fecha_creacion": datetime.now()
                }
            )
        return {"message": "Usuario registrado exitosamente"}
    except HTTPException:
        raise
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al registrar el usuario")