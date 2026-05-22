#AQUI VA LO QUE SE VA A PERSISITIR EN LA BASE DE DATOS (CRUD)
import traceback
from datetime import datetime

from fastapi import HTTPException, Depends
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
    
async def actualizar_usuario(datos: dict, current_user: dict):
    id_usuario = current_user["id_usuario"]
    with engine.connect() as db:
        try:
            db.execute(text("""
                UPDATE USUARIO
                SET nombre = :nombre, apellidos = :apellidos, email = :email
                WHERE id_usuario = :id_usuario
            """), {**datos, "id_usuario": id_usuario})
            db.commit()
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    return {"mensaje": "Perfil actualizado correctamente"}

async def cambiar_contraseña(datos: dict, current_user: dict):
    id_usuario = current_user["id_usuario"]
    with engine.connect() as db:
        try:
            usuario = db.execute(text("""
                SELECT contraseña FROM USUARIO WHERE id_usuario = :id_usuario
            """), {"id_usuario": id_usuario}).fetchone()

            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            if not verificar_password(datos["contrasena_actual"], usuario.contraseña):
                raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

            db.execute(text("""
                UPDATE USUARIO SET contraseña = :nueva_contraseña WHERE id_usuario = :id_usuario
            """), {"nueva_contraseña": hashear_password(datos["nueva_contraseña"]), "id_usuario": id_usuario})

            db.commit()
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    return {"mensaje": "Contraseña actualizada correctamente"}


    id_usuario = current_user["id_usuario"]
    with engine.connect() as db:
        try:
            usuario = db.execute(text("""
                SELECT nombre, apellidos, email
                FROM USUARIO WHERE id_usuario = :id_usuario
            """), {"id_usuario": id_usuario}).fetchone()
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"usuario": dict(usuario._mapping)}

async def eliminar_usuario(current_user: dict):
    with engine.connect() as db:
        try:
            db.execute(text("""
                DELETE FROM USUARIO WHERE id_usuario = :id
            """), {"id": current_user["id_usuario"]})
            db.commit()
        except Exception as e:
            db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    return {"mensaje": "Cuenta eliminada"}