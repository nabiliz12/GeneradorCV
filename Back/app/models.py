from pydantic import BaseModel


class ForumData(BaseModel):
    nombre: str
    email: str
    experiencia: str