from io import BytesIO

from fastapi import Body, Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fpdf import FPDF
from pydantic import BaseModel
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient


# & c:\Users\nabil.bouihia\CV_Boost\Back\.venv\Scripts\Activate.ps1
#python -m uvicorn app.main:app --reload --port 8001



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# conectar mongodb

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["CvBoostDataBase"]
collection = db["formulario"]


# esto es una prueba
@app.get("/")
def read_root():
    return {"message": "Hola FastAPI"}


class FormularioDatos(BaseModel):
    nombre: str
    email: str
    experiencia: str

# Ruta post para recibir formulario


@app.post("/api/form")
async def recibir_formulario(data: FormularioDatos):
    print("DATA RECIBIDA:", data.dict())
    await collection.insert_one(data.dict())
    return {"mensaje": "Formulario recibido", "data": data}


@app.get("/api/form")
async def listar_formularios():
    docs = []
    cursor = collection.find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # convertir ObjectId a string
        docs.append(doc)
    return {"formularios": docs}


@app.post("/api/form/descargarpdf")
async def descargarPDf(data: FormularioDatos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(0, 10, f"Nombre: {data.nombre}", ln=True)
    pdf.cell(0, 10, f"Email: {data.email}", ln=True)
    pdf.multi_cell(0, 10, f"Experiencia: {data.experiencia}")

    # Guardar PDF en un buffer de memoria
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    # Devolver PDF como StreamingResponse
    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=formulario.pdf"
    })
