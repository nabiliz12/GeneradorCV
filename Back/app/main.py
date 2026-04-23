from io import BytesIO

from fastapi import FastAPI
# from fastapi.datastructures import FormData
from fastapi.middleware.cors import CORSMiddleware

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


# & c:\Users\nabil.bouihia\CV_Boost\Back\.venv\Scripts\Activate.ps1
#python -m uvicorn app.main:app --reload --port 8001

#pip install fastapi uvicorn sqlalchemy pymysql
#pip install pymongo
#pip install fpdf
#pip install motor

app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

# conectar mongodb
# MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# client = AsyncIOMotorClient(MONGO_URL)
# db = client["CvBoostDataBase"]
# collection = db["formulario"]

# conectar MYSQL
# DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:abc123.@localhost:3306/cvboostdatabase1")
# engine = create_engine(DATABASE_URL)


# Ruta post para recibir formulario

@app.post("/api/formulario")
async def recibir_formulario(datos: FormDataModel):
    
    print("DATA RECIBIDA:", datos)
    # await collection.insert_one(datos.dict())
    # db=engine.connect()
    
    # query = text("""INSERT INTO forms (nombre, email, experiencia)VALUES (:nombre, :email, :experiencia)""")
    
    # # db.execute(query, {"nombre": data.nombre, "email": data.email, "experiencia": data.experiencia})
    # # db.commit()
    # # db.close()

    return {"mensaje": "Formulario recibido", "data": datos}


# @app.get("/api/form")
# async def listar_formularios():
#     docs = []
#     cursor = collection.find({})
#     async for doc in cursor:
#         doc["_id"] = str(doc["_id"])  # convertir ObjectId a string
#         docs.append(doc)
#     return {"formularios": docs}


# @app.post("/api/form/descargarpdf")
# async def descargarPDf(data: FormDataModel):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
    
#     pdf.cell(0, 10, f"Nombre: {data.nombre}", ln=True)
#     pdf.cell(0, 10, f"Email: {data.email}", ln=True)
#     pdf.multi_cell(0, 10, f"Experiencia: {data.experiencia}")

#     # Guardar PDF en un buffer de memoria
#     buffer = BytesIO()
#     pdf.output(buffer)
#     buffer.seek(0)

#     # Devolver PDF como StreamingResponse
#     return StreamingResponse(buffer, media_type="application/pdf", headers={
#         "Content-Disposition": "attachment; filename=formulario.pdf"
#     })
    
    
