from pydantic import BaseModel


class FormDataModel(BaseModel):
    nombre: str
    email: str
    experiencia: str