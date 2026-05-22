from fastapi import APIRouter, Depends, Body
from app.core.database import engine
from app.services.auth_service import get_current_user
from app.models.models import FormDataModel
from app.services import cv_service

app = APIRouter()

@app.post("/cv")
async def guardarCV(datos: FormDataModel, current_user: dict = Depends(get_current_user)):
    return await cv_service.guardar_cv(datos, current_user["id_usuario"])
    
@app.get("/recuperar_cv/{id_cv}")
async def recuperar_cv(id_cv: int, current_user: dict = Depends(get_current_user)):
    return await cv_service.recuperar_cv(id_cv, current_user["id_usuario"])

@app.post("/editar_cv/{id_cv}")
async def editar_cv(id_cv: int, datos: dict = Body(...), current_user: dict = Depends(get_current_user)):
    return await cv_service.editar_cv(id_cv, datos, current_user["id_usuario"])
    
@app.delete("/historial/eliminar/{id_cv}")
async def eliminar_cv(id_cv: int, current_user: dict = Depends(get_current_user)):
    return await cv_service.eliminar_cv(id_cv, current_user["id_usuario"])
    
@app.get("/historial")
async def obtener_historial(current_user: dict = Depends(get_current_user)):
    return await cv_service.obtener_historial(current_user["id_usuario"])
