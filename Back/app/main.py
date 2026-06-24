from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth as registro
from app.routers import cv
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://generadorcv.vercel.app",
        "https://generador-cv-six.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(registro.app, prefix="/api/auth", tags=["auth"])
app.include_router(cv.app, prefix="/api", tags=["cv"])

#python -m uvicorn app.main:app --reload --port 8001