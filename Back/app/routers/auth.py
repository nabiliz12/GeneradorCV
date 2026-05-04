from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


# pip install python-jose[cryptography] passlib[bcrypt]
 #instalarlo 
SECRET_KEY = "cambia_esto_por_algo_seguro_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 día

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def hashear_password(contrasena: str) -> str:
    return pwd_context.hash(contrasena)

def verificar_password(contrasena: str, hashed: str) -> bool:
    return pwd_context.verify(contrasena, hashed)

def crear_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None