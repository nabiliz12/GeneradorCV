import traceback
from fastapi import HTTPException
from sqlalchemy import text
from app.core.database import engine


def verificar_pertenencia(id_cv: int, id_usuario: int):
    with engine.connect() as db:
        cv = db.execute(text("""
            SELECT id_cv FROM CURRICULUM WHERE id_cv=:id_cv AND id_usuario=:id_usuario
        """), {"id_cv": id_cv, "id_usuario": id_usuario}).fetchone()
        if not cv:
            raise HTTPException(status_code=404, detail="CV no encontrado o no pertenece al usuario")


def insertar_curriculum(datos, id_usuario: int) -> int:
    with engine.connect() as db:
        result = db.execute(text("""
            INSERT INTO CURRICULUM (id_usuario, titulo, tiene_foto, plantilla)
            VALUES (:id_usuario, :titulo, :tiene_foto, :plantilla)
        """), {
            "id_usuario": id_usuario,
            "titulo": f"CV de {datos.datosPersonales.nombre} {datos.datosPersonales.apellido}",
            "tiene_foto": 1 if datos.foto else 0,
            "plantilla": datos.plantilla or None
        })
        db.commit()
        return result.lastrowid

def insertar_foto(id_cv: int, foto_base64: str):
    with engine.connect() as db:
        db.execute(text("""
            UPDATE CURRICULUM SET foto_base64=:foto_base64, tiene_foto=1 WHERE id_cv=:id_cv
        """), {"foto_base64": foto_base64, "id_cv": id_cv})
        db.commit()

def insertar_datos_personales(id_cv: int, datos):
    with engine.connect() as db:
        db.execute(text("""
            INSERT INTO DATOS_PERSONALES
            (id_cv, nombre, apellido, email, telefono, direccion, codigo_postal, localidad, permiso_conducir)
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
        db.commit()


def insertar_educacion(id_cv: int, educacion: list):
    filtrada = [e for e in educacion if e.titulo or e.institucion]
    if not filtrada:
        return
    with engine.connect() as db:
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
            for e in filtrada
        ])
        db.commit()


def insertar_certificaciones(id_cv: int, certificaciones: list):
    filtradas = [c for c in certificaciones if c.certificacion]
    if not filtradas:
        return
    with engine.connect() as db:
        db.execute(text("""
            INSERT INTO CERTIFICACION (id_cv, certificacion, expedicion)
            VALUES (:id_cv, :certificacion, :expedicion)
        """), [
            {
                "id_cv": id_cv,
                "certificacion": c.certificacion,
                "expedicion": f"{c.mes} {c.anio}".strip() or None
            }
            for c in filtradas
        ])
        db.commit()


def insertar_experiencia(id_cv: int, experiencia: list):
    filtrada = [e for e in experiencia if e.cargo or e.empresa]
    if not filtrada:
        return
    with engine.connect() as db:
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
            for e in filtrada
        ])
        db.commit()


def insertar_idiomas(id_cv: int, idiomas: list):
    filtrados = [i for i in idiomas if i.idioma]
    if not filtrados:
        return
    with engine.connect() as db:
        db.execute(text("""
            INSERT INTO IDIOMA (id_cv, nombre, nivel) VALUES (:id_cv, :nombre, :nivel)
        """), [{"id_cv": id_cv, "nombre": i.idioma, "nivel": i.nivel} for i in filtrados])
        db.commit()


def insertar_skills(id_cv: int, skills: list):
    with engine.connect() as db:
        for skill_nombre in skills:
            db.execute(text("INSERT IGNORE INTO HABILIDAD (nombre) VALUES (:nombre)"), {"nombre": skill_nombre})
            row = db.execute(text("SELECT id_habilidad FROM HABILIDAD WHERE nombre=:nombre"), {"nombre": skill_nombre}).fetchone()
            db.execute(text("INSERT IGNORE INTO CV_HABILIDAD (id_cv, id_habilidad) VALUES (:id_cv, :id_habilidad)"),
                       {"id_cv": id_cv, "id_habilidad": row[0]})
        db.commit()


def insertar_oferta(id_cv: int, oferta):
    if not (oferta.empresa or oferta.descripcion):
        return
    with engine.connect() as db:
        result = db.execute(text("""
            INSERT INTO OFERTA_EMPLEO (titulo, empresa, descripcion)
            VALUES (:titulo, :empresa, :descripcion)
        """), {
            "titulo": f"Oferta - {oferta.empresa}",
            "empresa": oferta.empresa,
            "descripcion": oferta.descripcion
        })
        db.execute(text("UPDATE CURRICULUM SET id_oferta=:id_oferta WHERE id_cv=:id_cv"),
                   {"id_oferta": result.lastrowid, "id_cv": id_cv})
        db.commit()


def actualizar_ia(id_cv: int, descripcion: str, porcentaje):
    with engine.connect() as db:
        db.execute(text("""
            UPDATE CURRICULUM SET descripcion=:descripcion, porcentaje=:porcentaje WHERE id_cv=:id_cv
        """), {"descripcion": descripcion, "porcentaje": porcentaje, "id_cv": id_cv})
        db.commit()



def obtener_cv_completo(id_cv: int, id_usuario: int) -> dict:
    with engine.connect() as db:
        curriculum = db.execute(text("""
            SELECT tiene_foto, descripcion, porcentaje, plantilla, foto_base64 FROM CURRICULUM
            WHERE id_cv=:id_cv AND id_usuario=:id_usuario
        """), {"id_cv": id_cv, "id_usuario": id_usuario}).fetchone()
        if not curriculum:
            raise HTTPException(status_code=404, detail="CV no encontrado")

        datos       = db.execute(text("SELECT nombre, apellido, email, telefono, direccion, codigo_postal, localidad, permiso_conducir FROM DATOS_PERSONALES WHERE id_cv=:id_cv"), {"id_cv": id_cv}).fetchone()
        educacion   = db.execute(text("SELECT institucion, titulo, anioInicio, anioFin FROM EDUCACION WHERE id_cv=:id_cv"), {"id_cv": id_cv}).fetchall()
        certs       = db.execute(text("SELECT certificacion, expedicion FROM CERTIFICACION WHERE id_cv=:id_cv"), {"id_cv": id_cv}).fetchall()
        experiencia = db.execute(text("SELECT empresa, puesto, fecha_inicio, fecha_fin, descripcion FROM EXPERIENCIA_LABORAL WHERE id_cv=:id_cv"), {"id_cv": id_cv}).fetchall()
        idiomas     = db.execute(text("SELECT nombre, nivel FROM IDIOMA WHERE id_cv=:id_cv"), {"id_cv": id_cv}).fetchall()
        skills      = db.execute(text("SELECT h.nombre FROM CV_HABILIDAD cvh JOIN HABILIDAD h ON cvh.id_habilidad=h.id_habilidad WHERE cvh.id_cv=:id_cv"), {"id_cv": id_cv}).fetchall()
        oferta      = db.execute(text("SELECT o.titulo, o.empresa, o.descripcion FROM CURRICULUM c LEFT JOIN OFERTA_EMPLEO o ON c.id_oferta=o.id_oferta WHERE c.id_cv=:id_cv"), {"id_cv": id_cv}).fetchone()

    return {
        "id_cv": id_cv,
        "datosPersonales": dict(datos._mapping),
        "educacion": [dict(r._mapping) for r in educacion],
        "certificaciones": [dict(r._mapping) for r in certs],
        "experiencia": [dict(r._mapping) for r in experiencia],
        "idiomas": [dict(r._mapping) for r in idiomas],
        "skills": [r.nombre for r in skills],
        "ofertaDeTrabajo": dict(oferta._mapping) if oferta and oferta.empresa else {},
        "foto": bool(curriculum.tiene_foto),
        "descripcion": curriculum.descripcion,
        "porcentaje": int(curriculum.porcentaje) if curriculum.porcentaje is not None else None,
        "plantilla": curriculum.plantilla,
        "foto_base64": curriculum.foto_base64,
    }


def obtener_historial(id_usuario: int):
    with engine.connect() as db:
        cvs = db.execute(text("""
            SELECT c.id_cv, c.titulo, c.fecha_creacion, o.empresa AS empresa_oferta
            FROM CURRICULUM c
            LEFT JOIN OFERTA_EMPLEO o ON c.id_oferta=o.id_oferta
            WHERE c.id_usuario=:id_usuario
            ORDER BY c.fecha_creacion DESC
        """), {"id_usuario": id_usuario}).fetchall()
    return {"cvs": [dict(r._mapping) for r in cvs]}


def eliminar_cv(id_cv: int):
    with engine.connect() as db:
        db.execute(text("DELETE FROM CURRICULUM WHERE id_cv=:id_cv"), {"id_cv": id_cv})
        db.commit()


def actualizar_datos_personales(id_cv: int, dp: dict):
    with engine.connect() as db:
        db.execute(text("""
            UPDATE DATOS_PERSONALES
            SET nombre=:nombre, apellido=:apellido, email=:email,
                telefono=:telefono, direccion=:direccion,
                codigo_postal=:codigo_postal, localidad=:localidad,
                permiso_conducir=:permiso_conducir
            WHERE id_cv=:id_cv
        """), {
            "id_cv": id_cv,
            "nombre": dp.get("nombre"),
            "apellido": dp.get("apellido"),
            "email": dp.get("email"),
            "telefono": dp.get("telefono"),
            "direccion": dp.get("direccion"),
            "codigo_postal": dp.get("codigo_postal"),       
            "localidad": dp.get("localidad"),
            "permiso_conducir": dp.get("permiso_conducir"), 
        })
        db.commit()


def reemplazar_educacion(id_cv: int, educacion: list):
    with engine.connect() as db:
        db.execute(text("DELETE FROM EDUCACION WHERE id_cv=:id_cv"), {"id_cv": id_cv})
        filtrada = [e for e in educacion if e.get("titulo") or e.get("institucion")]
        if filtrada:
            db.execute(text("""
                INSERT INTO EDUCACION (id_cv, institucion, titulo, anioInicio, anioFin)
                VALUES (:id_cv, :institucion, :titulo, :anioInicio, :anioFin)
            """), [
                {
                    "id_cv": id_cv,
                    "institucion": e.get("institucion"),
                    "titulo": e.get("titulo"),
                    "anioInicio": e.get("anioInicio"),  
                    "anioFin": e.get("anioFin"),
                }
                for e in filtrada
            ])
        db.commit()


def reemplazar_experiencia(id_cv: int, experiencia: list):
    with engine.connect() as db:
        db.execute(text("DELETE FROM EXPERIENCIA_LABORAL WHERE id_cv=:id_cv"), {"id_cv": id_cv})
        filtrada = [e for e in experiencia if e.get("puesto") or e.get("empresa")] 
        if filtrada:
            db.execute(text("""
                INSERT INTO EXPERIENCIA_LABORAL (id_cv, empresa, puesto, fecha_inicio, fecha_fin)
                VALUES (:id_cv, :empresa, :puesto, :fecha_inicio, :fecha_fin)
            """), [
                {
                    "id_cv": id_cv,
                    "empresa": e.get("empresa"),
                    "puesto": e.get("puesto"),            
                    "fecha_inicio": e.get("fecha_inicio"),
                    "fecha_fin": e.get("fecha_fin"),
                }
                for e in filtrada
            ])
        db.commit()


def reemplazar_idiomas(id_cv: int, idiomas: list):
    with engine.connect() as db:
        db.execute(text("DELETE FROM IDIOMA WHERE id_cv=:id_cv"), {"id_cv": id_cv})
        filtrados = [i for i in idiomas if i.get("nombre")] 
        if filtrados:
            db.execute(text("INSERT INTO IDIOMA (id_cv, nombre, nivel) VALUES (:id_cv, :nombre, :nivel)"),
                       [{"id_cv": id_cv, "nombre": i["nombre"], "nivel": i.get("nivel")} for i in filtrados])
        db.commit()


def reemplazar_certificaciones(id_cv: int, certs: list):
    with engine.connect() as db:
        db.execute(text("DELETE FROM CERTIFICACION WHERE id_cv=:id_cv"), {"id_cv": id_cv})
        filtradas = [c for c in certs if c.get("certificacion")]
        if filtradas:
            db.execute(text("INSERT INTO CERTIFICACION (id_cv, certificacion, expedicion) VALUES (:id_cv, :certificacion, :expedicion)"),
                       [{"id_cv": id_cv, "certificacion": c["certificacion"], "expedicion": c.get("expedicion")} for c in filtradas])
        db.commit()


def reemplazar_skills(id_cv: int, skills: list):
    with engine.connect() as db:
        db.execute(text("DELETE FROM CV_HABILIDAD WHERE id_cv=:id_cv"), {"id_cv": id_cv})
        for skill_nombre in skills:
            db.execute(text("INSERT IGNORE INTO HABILIDAD (nombre) VALUES (:nombre)"), {"nombre": skill_nombre})
            row = db.execute(text("SELECT id_habilidad FROM HABILIDAD WHERE nombre=:nombre"), {"nombre": skill_nombre}).fetchone()
            db.execute(text("INSERT IGNORE INTO CV_HABILIDAD (id_cv, id_habilidad) VALUES (:id_cv, :id_habilidad)"),
                       {"id_cv": id_cv, "id_habilidad": row[0]})
        db.commit()  
    
