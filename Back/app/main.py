from io import BytesIO
import os
import traceback

from fastapi import FastAPI, HTTPException
# from fastapi.datastructures import FormData
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

from app.models import FormDataModel

from app.models import FormDataModel
# from fastapi.responses import StreamingResponse
#from fpdf import FPDF
# from pydantic import BaseModel
# from pymongo import MongoClient
# from motor.motor_asyncio import AsyncIOMotorClient
# from sqlalchemy import create_engine, text
# import os
# from app.models import FormDataModel
from app.routers import registro

# & c:\Users\nabil.bouihia\CV_Boost\Back\.venv\Scripts\Activate.ps1
#python -m uvicorn app.main:app --reload --port 8001

#pip install fastapi uvicorn sqlalchemy pymysql
#pip install pymongo
#pip install fpdf
#pip install motor

app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

app.include_router(registro.router,prefix="/api/auth", tags=["auth"])

# conectar mongodb
# MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# client = AsyncIOMotorClient(MONGO_URL)
# db = client["CvBoostDataBase"]
# collection = db["formulario"]

# conectar MYSQL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:abc123.@localhost:3306/cv_generator")
engine = create_engine(DATABASE_URL)


@app.post("/api/formulario")
async def guardarFormulario(datos: FormDataModel):
    print("DATA RECIBIDA:", datos)

    with engine.connect() as db:
        try:
            # 1. Crear registro en CURRICULUM (necesario para obtener id_cv)
            result = db.execute(text("""
                INSERT INTO CURRICULUM (id_usuario, titulo, tiene_foto)
                VALUES (1, :titulo, :tiene_foto)
            """), {
                "titulo": f"CV de {datos.datosPersonales.nombre} {datos.datosPersonales.apellido}",
                "tiene_foto": 1 if datos.foto else 0
            })
            id_cv = result.lastrowid  # ← clave para todo lo demás

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
            if datos.educacion:
                db.execute(text("""
                    INSERT INTO EDUCACION (id_cv, institucion, titulo, anioInicio, anioFin)
                    VALUES (:id_cv, :institucion, :titulo, :anioInicio, :anioFin)
                """), [
                    {
                        "id_cv": id_cv,
                        "institucion": e.institucion,
                        "titulo": e.titulo,
                        "anioInicio": e.anioInicio or None,
                        "anioFin": e.anioFin or None
                    }
                    for e in datos.educacion
                ])

            # 4. Certificaciones
            if datos.certificaciones:
                db.execute(text("""
                    INSERT INTO CERTIFICACION (id_cv, certificacion, expedicion)
                    VALUES (:id_cv, :certificacion, :expedicion)
                """), [
                    {
                        "id_cv": id_cv,
                        "certificacion": c.certificacion,
                        "expedicion": c.expedicion
                    }
                    for c in datos.certificaciones
                ])

            # 5. Experiencia laboral
            if datos.experiencia:
                db.execute(text("""
                    INSERT INTO EXPERIENCIA_LABORAL (id_cv, empresa, puesto, fecha_inicio, fecha_fin)
                    VALUES (:id_cv, :empresa, :puesto, :fecha_inicio, :fecha_fin)
                """), [
                    {
                        "id_cv": id_cv,
                        "empresa": e.empresa,
                        "puesto": e.cargo,        # "cargo" en Vue → "puesto" en BD
                        "fecha_inicio": e.anioInicio or None,
                        "fecha_fin": e.anioFin or None
                    }
                    for e in datos.experiencia
                ])

            # 6. Idiomas
            if datos.idiomas:
                db.execute(text("""
                    INSERT INTO IDIOMA (id_cv, nombre, nivel)
                    VALUES (:id_cv, :nombre, :nivel)
                """), [
                    {
                        "id_cv": id_cv,
                        "nombre": i.idioma,       # "idioma" en Vue → "nombre" en BD
                        "nivel": i.nivel
                    }
                    for i in datos.idiomas
                ])

            # 7. Skills (N:M → primero HABILIDAD, luego CV_HABILIDAD)
            for skill_nombre in datos.skills:
                # INSERT OR IGNORE para no romper si ya existe
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
                # Vincular la oferta al curriculum
                db.execute(text("""
                    UPDATE CURRICULUM SET id_oferta = :id_oferta WHERE id_cv = :id_cv
                """), {"id_oferta": oferta_result.lastrowid, "id_cv": id_cv})

            db.commit()

        except Exception as e:
            db.rollback()
            traceback.print_exc() 
            raise HTTPException(status_code=500, detail=str(e))

    return {"mensaje": "CV guardado correctamente", "id_cv": id_cv}


@app.get("/api/recuperar_cv/{id_cv}")
async def recuperar_cv(id_cv: int):
    with engine.connect() as db:
        try:
            # 1. Datos personales
            datos = db.execute(text("""
                SELECT nombre, Apellido, email, telefono, direccion, 
                       codigo_postal, localidad, permiso_conducir
                FROM DATOS_PERSONALES WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchone()

            if not datos:
                raise HTTPException(status_code=404, detail="CV no encontrado")

            # 2. Educación
            educacion = db.execute(text("""
                SELECT institucion, titulo, anioInicio, anioFin
                FROM EDUCACION WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            # 3. Certificaciones
            certificaciones = db.execute(text("""
                SELECT certificacion, expedicion
                FROM CERTIFICACION WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            # 4. Experiencia laboral
            experiencia = db.execute(text("""
                SELECT empresa, puesto, fecha_inicio, fecha_fin, descripcion
                FROM EXPERIENCIA_LABORAL WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            # 5. Idiomas
            idiomas = db.execute(text("""
                SELECT nombre, nivel
                FROM IDIOMA WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            # 6. Skills
            skills = db.execute(text("""
                SELECT h.nombre
                FROM CV_HABILIDAD cvh
                JOIN HABILIDAD h ON cvh.id_habilidad = h.id_habilidad
                WHERE cvh.id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchall()

            # 7. Oferta de trabajo (a través de CURRICULUM)
            oferta = db.execute(text("""
                SELECT o.titulo, o.empresa, o.descripcion
                FROM CURRICULUM c
                LEFT JOIN OFERTA_EMPLEO o ON c.id_oferta = o.id_oferta
                WHERE c.id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchone()

            # 8. Foto
            curriculum = db.execute(text("""
                SELECT tiene_foto FROM CURRICULUM WHERE id_cv = :id_cv
            """), {"id_cv": id_cv}).fetchone()

        except HTTPException:
            raise
        except Exception as e:
            import traceback
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
        "foto": bool(curriculum.tiene_foto) if curriculum else False
    }