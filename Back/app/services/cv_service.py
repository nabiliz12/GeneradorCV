from fastapi import HTTPException
from app.repositories import cv_repository
from app.services.ia_service import implementar_IA



async def guardar_cv(datos, id_usuario: int):
    id_cv = cv_repository.insertar_curriculum(datos, id_usuario)
    cv_repository.insertar_datos_personales(id_cv, datos)
    cv_repository.insertar_educacion(id_cv, datos.educacion)
    cv_repository.insertar_certificaciones(id_cv, datos.certificaciones)
    cv_repository.insertar_experiencia(id_cv, datos.experiencia)
    cv_repository.insertar_idiomas(id_cv, datos.idiomas)
    cv_repository.insertar_skills(id_cv, datos.skills)
    if datos.foto:
        cv_repository.insertar_foto(id_cv, datos.foto_base64)
        
    cv_repository.insertar_oferta(id_cv, datos.ofertaDeTrabajo)

    textoDescripcion, porcentaje = await implementar_IA(datos.dict())
    cv_repository.actualizar_ia(id_cv, textoDescripcion, porcentaje)

    return {"mensaje": "CV guardado correctamente", "id_cv": id_cv}


async def recuperar_cv(id_cv: int, id_usuario: int):
    return cv_repository.obtener_cv_completo(id_cv, id_usuario)


async def editar_cv(id_cv: int, datos: dict, id_usuario: int):
    cv_repository.verificar_pertenencia(id_cv, id_usuario)
    cv_repository.actualizar_datos_personales(id_cv, datos["datosPersonales"])
    cv_repository.reemplazar_educacion(id_cv, datos.get("educacion", []))
    cv_repository.reemplazar_experiencia(id_cv, datos.get("experiencia", []))
    cv_repository.reemplazar_idiomas(id_cv, datos.get("idiomas", []))
    cv_repository.reemplazar_certificaciones(id_cv, datos.get("certificaciones", []))
    cv_repository.reemplazar_skills(id_cv, datos.get("skills", []))

    textoDescripcion, porcentaje = await implementar_IA(datos)
    cv_repository.actualizar_ia(id_cv, textoDescripcion, porcentaje)

    return {"mensaje": "CV actualizado correctamente", "id_cv": id_cv}


async def obtener_historial(id_usuario: int):
    return cv_repository.obtener_historial(id_usuario)


async def eliminar_cv(id_cv: int, id_usuario: int):
    cv_repository.verificar_pertenencia(id_cv, id_usuario)
    cv_repository.eliminar_cv(id_cv)
    return {"mensaje": "CV eliminado correctamente"}

