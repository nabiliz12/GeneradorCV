from fastapi import Body, Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hola FastAPI"}

class FormularioDatos(BaseModel):
    nombre: str
    email: str
    experiencia: str
# Ruta POST para recibir formulario

@app.post("/api/form")
async def recibir_formulario(data: FormularioDatos):
    print("DATA RECIBIDA:", data.dict())
    return {"mensaje": "Formulario recibido", "data": data}