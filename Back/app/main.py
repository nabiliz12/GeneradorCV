from io import BytesIO
import os
import traceback

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from app.routers.auth import hashear_password, verificar_password
import asyncio
from app.models import FormDataModel
from app.routers import registro
from groq import Groq

app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

app.include_router(registro.router,prefix="/api/auth", tags=["auth"])

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:abc123.@localhost:3306/cv_generator")
engine = create_engine(DATABASE_URL)


@app.post("/api/cv")
async def guardarCV(datos: FormDataModel, current_user: dict = Depends(registro.get_current_user)):
    print("CURRENT USER:", current_user)
    id_usuario = current_user["id_usuario"]
    print("ID USUARIO:", id_usuario)
    print("DATA RECIBIDA:", datos)

    with engine.connect() as db:
        try:
            # 1. CURRICULUM
            result = db.execute(text("""
                INSERT INTO CURRICULUM (id_usuario, titulo, tiene_foto)
                VALUES (:id_usuario, :titulo, :tiene_foto)
            """), {
                "id_usuario": id_usuario,
                "titulo": f"CV de {datos.datosPersonales.nombre} {datos.datosPersonales.apellido}",
                "tiene_foto": 1 if datos.foto else 0
            })
            id_cv = result.lastrowid

            # 2. Datos personales
            db.execute(text("""
                INSERT INTO DATOS_PERSONALES
                (id_cv, nombre, Apellido, email, telefono, direccion, codigo_postal, localidad, permiso_conducir)
                VALUES (:id_cv, :nombre, :apellido, :email, :telefono, :direccion, :codigo_postal, :localidad, :permiso_conducir)
            """), {
                "id_cv": id_cv,
                "nombre": datos.datosPersonales.nombre,
                "apellido": datos.datosPersonales.apellido,
                "email": datos.datosPersonales.email,
                "telefono": datos.datosPersonales.telefono,
                "direccion": datos.datosPersonales.direccion,
                "codigo_postal": datos.datosPersonales.codigoPostal,
                "localidad": datos.datosPersonales.localidad,
                "permiso_conducir": datos.datosPersonales.permisoConducir
            })

            # 3. Educación
            educacion_filtrada = [e for e in datos.educacion if e.titulo or e.institucion]
            if educacion_filtrada:
                db.execute(text("""
                    INSERT INTO EDUCACION (id_cv, institucion, titulo, anioInicio, anioFin)
                    VALUES (:id_cv, :institucion, :titulo, :anioInicio, :anioFin)
                """), [
                    {
                        "id_cv": id_cv,
                        "institucion": e.institucion,
                        "titulo": e.titulo,
                        "anioInicio": f"{e.mesInicio} {e.anioInicio}".strip() or None,
                        "anioFin": "Actualidad" if e.actualidad else f"{e.mesFin} {e.anioFin}".strip() or None
                    }
                    for e in educacion_filtrada
                ])

            # 4. Certificaciones
            certificaciones_filtradas = [c for c in datos.certificaciones if c.certificacion]
            if certificaciones_filtradas:
                db.execute(text("""
                    INSERT INTO CERTIFICACION (id_cv, certificacion, expedicion)
                    VALUES (:id_cv, :certificacion, :expedicion)
                """), [
                    {
                        "id_cv": id_cv,
                        "certificacion": c.certificacion,
                        "expedicion": f"{c.mes} {c.anio}".strip() or None
                    }
                    for c in certificaciones_filtradas
                ])

            # 5. Experiencia laboral
            experiencia_filtrada = [e for e in datos.experiencia if e.cargo or e.empresa]
            if experiencia_filtrada:
                db.execute(text("""
                    INSERT INTO EXPERIENCIA_LABORAL (id_cv, empresa, puesto, fecha_inicio, fecha_fin)
                    VALUES (:id_cv, :empresa, :puesto, :fecha_inicio, :fecha_fin)
                """), [
                    {
                        "id_cv": id_cv,
                        "empresa": e.empresa,
                        "puesto": e.cargo,
                        "fecha_inicio": f"{e.mesInicio} {e.anioInicio}".strip() or None,
                        "fecha_fin": "Actualidad" if e.actualidad else f"{e.mesFin} {e.anioFin}".strip() or None
                    }
                    for e in experiencia_filtrada
                ])

            # 6. Idiomas
            idiomas_filtrados = [i for i in datos.idiomas if i.idioma]
            if idiomas_filtrados:
                db.execute(text("""
                    INSERT INTO IDIOMA (id_cv, nombre, nivel)
                    VALUES (:id_cv, :nombre, :nivel)
                """), [
                    {
                        "id_cv": id_cv,
                        "nombre": i.idioma,
                        "nivel": i.nivel
                    }
                    for i in idiomas_filtrados
                ])

            # 7. Skills
            for skill_nombre in datos.skills:
                db.execute(text("""
                    INSERT IGNORE INTO HABILIDAD (nombre) VALUES (:nombre)
                """), {"nombre": skill_nombre})

                skill_result = db.execute(text("""
                    SELECT id_habilidad FROM HABILIDAD WHERE nombre = :nombre
                """), {"nombre": skill_nombre})
                id_habilidad = skill_result.fetchone()[0]

                db.execute(text("""
                    INSERT IGNORE INTO CV_HABILIDAD (id_cv, id_habilidad)
                    VALUES (:id_cv, :id_habilidad)
                """), {"id_cv": id_cv, "id_habilidad": id_habilidad})

            # 8. Oferta de trabajo
            if datos.ofertaDeTrabajo.empresa or datos.ofertaDeTrabajo.descripcion:
                oferta_result = db.execute(text("""
                    INSERT INTO OFERTA_EMPLEO (titulo, empresa, descripcion)
                    VALUES (:titulo, :empresa, :descripcion)
                """), {
                    "titulo": f"Oferta - {datos.ofertaDeTrabajo.empresa}",
                    "empresa": datos.ofertaDeTrabajo.empresa,
                    "descripcion": datos.ofertaDeTrabajo.descripcion
                })
                db.execute(text("""
                    UPDATE CURRICULUM SET id_oferta = :id_oferta WHERE id_cv = :id_cv
                """), {"id_oferta": oferta_result.lastrowid, "id_cv": id_cv})

            #9 Implementación IA
            textoDescripcion = await implementar_IA(datos.dict(),current_user)
            db.execute(text("""
                            UPDATE CURRICULUM SET descripcion = :textoDescripcion WHERE id_cv = :id_cv
                            """), {"textoDescripcion": textoDescripcion, "id_cv": id_cv})

            db.commit()

        except Exception as e:
            db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    return {"mensaje": "CV guardado correctamente", "id_cv": id_cv}

@app.get("/api/recuperar_cv/{id_cv}")
async def recuperar_cv(id_cv: int, current_user: dict = Depends(registro.get_current_user)):
    id_usuario = current_user["id_usuario"]
    with engine.connect() as db:
        try:
            # Verificar que el CV pertenece al usuario
            cv_check = db.execute(text("""
                SELECT id_cv FROM CURRICULUM
                WHERE id_cv = :id_cv AND id_usuario = :id_usuario
            """), {"id_cv": id_cv, "id_usuario": id_usuario}).fetchone()

            if not cv_check:
                raise HTTPException(status_code=404, detail="CV no encontrado")

            # A partir de aquí solo filtramos por id_cv (ya verificamos el usuario arriba)
            datos = db.execute(text("""
                SELECT nombre, Apellido, email, telefono, direccion,
                       codigo_postal, localidad, permiso_conducir
                FROM DATOS_PERSONALES WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchone()

            educacion = db.execute(text("""
                SELECT institucion, titulo, anioInicio, anioFin
                FROM EDUCACION WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            certificaciones = db.execute(text("""
                SELECT certificacion, expedicion
                FROM CERTIFICACION WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            experiencia = db.execute(text("""
                SELECT empresa, puesto, fecha_inicio, fecha_fin, descripcion
                FROM EXPERIENCIA_LABORAL WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            idiomas = db.execute(text("""
                SELECT nombre, nivel
                FROM IDIOMA WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            skills = db.execute(text("""
                SELECT h.nombre
                FROM CV_HABILIDAD cvh
                JOIN HABILIDAD h ON cvh.id_habilidad = h.id_habilidad
                WHERE cvh.id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            oferta = db.execute(text("""
                SELECT o.titulo, o.empresa, o.descripcion
                FROM CURRICULUM c
                LEFT JOIN OFERTA_EMPLEO o ON c.id_oferta = o.id_oferta
                WHERE c.id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchone()

            curriculum = db.execute(text("""
                SELECT tiene_foto, descripcion FROM CURRICULUM WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchone()

        except HTTPException:
            raise
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    return {
        "id_cv": id_cv,
        "datosPersonales": dict(datos._mapping),
        "educacion": [dict(r._mapping) for r in educacion],
        "certificaciones": [dict(r._mapping) for r in certificaciones],
        "experiencia": [dict(r._mapping) for r in experiencia],
        "idiomas": [dict(r._mapping) for r in idiomas],
        "skills": [r.nombre for r in skills],
        "ofertaDeTrabajo": dict(oferta._mapping) if oferta and oferta.empresa else {},
        "foto": bool(curriculum.tiene_foto) if curriculum else False,
        "descripcion": curriculum.descripcion if curriculum else None
    }

@app.get("/api/historial")
async def obtener_historial(current_user: dict = Depends(registro.get_current_user)):
    id_usuario = current_user["id_usuario"]
    with engine.connect() as db:
        try:
            cvs = db.execute(text("""
                SELECT c.id_cv, c.titulo, c.fecha_creacion,
                       o.empresa AS empresa_oferta
                FROM CURRICULUM c
                LEFT JOIN OFERTA_EMPLEO o ON c.id_oferta = o.id_oferta
                WHERE c.id_usuario = :id_usuario
                ORDER BY c.fecha_creacion DESC
            """), {"id_usuario": id_usuario}).fetchall()
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    return {"cvs": [dict(r._mapping) for r in cvs]}


@app.delete("/api/historial/eliminar/{id_cv}")
async def eliminar_cv(id_cv: int, current_user: dict = Depends(registro.get_current_user)):
    id_usuario = current_user["id_usuario"]
    with engine.connect() as db:
        try:
            cv = db.execute(text("""
                SELECT id_cv FROM CURRICULUM WHERE id_cv = :id_cv AND id_usuario = :id_usuario
            """), {"id_cv": id_cv, "id_usuario": id_usuario}).fetchone()

            if not cv:
                raise HTTPException(status_code=404, detail="CV no encontrado o no pertenece al usuario")

            db.execute(text("""
                DELETE FROM CURRICULUM WHERE id_cv = :id_cv
            """), {"id_cv": id_cv})
            db.commit()
        except HTTPException:
            raise
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    return {"mensaje": "CV eliminado correctamente"}


@app.get("/api/usuario/perfil")
async def obtener_perfil_usuario(current_user: dict = Depends(registro.get_current_user)):
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


@app.put("/api/usuario/perfil")
async def actualizar_perfil_usuario(datos: dict, current_user: dict = Depends(registro.get_current_user)):
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

@app.put("/api/usuario/cambiar_contraseña")
async def cambiar_contraseña(datos: dict, current_user: dict = Depends(registro.get_current_user)):

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



@app.delete("/api/usuario")
async def eliminar_cuenta(current_user: dict = Depends(registro.get_current_user)):
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


async def implementar_IA(datos: dict, current_user: dict = None):
    nombre = datos.get("datosPersonales", {}).get("nombre", "")
    apellido = datos.get("datosPersonales", {}).get("apellido", "")
    educacion = datos.get("educacion", [])
    experiencia = datos.get("experiencia", [])
    skills = datos.get("skills", [])
    idiomas = datos.get("idiomas", [])
    oferta = datos.get("ofertaDeTrabajo", {})

    prompt = f"""
    Eres un experto en recursos humanos. Escribe un párrafo de perfil profesional para el CV de {nombre} {apellido}.

    Datos del candidato:
    - Educación: {educacion}
    - Experiencia: {experiencia}
    - Skills: {skills}
    - Idiomas: {idiomas}
    {"- Orientado a este tipo de puesto: " + str(oferta.get("descripcion", "")) if oferta.get("descripcion") else ""}

    Instrucciones estrictas:
    - Escribe SOLO el párrafo, nada más
    - 3-5 líneas máximo
    - En primera persona
    - Tono profesional pero natural, nada robótico
    - Destaca las habilidades y experiencia más relevantes
    - NO menciones nombres de empresas, organizaciones ni productos
    - NO uses frases genéricas como "soy una persona apasionada y motivada"
    - NO uses asteriscos, markdown, títulos ni explicaciones
    - El resultado debe poder usarse en cualquier CV sin modificaciones
    """

    try:
        client = Groq(api_key="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")
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error en IA: {e}")
        return ""