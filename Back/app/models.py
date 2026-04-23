from pydantic import BaseModel

class DatosPersonales(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion: str
    codigoPostal: str
    localidad: str
    permisoConducir: bool
    
class Educacion(BaseModel):
    institucion: str
    titulo: str
    anioInicio: str
    anioFin: str

class Certificacion(BaseModel):
    certificacion: str
    expedicion: str

class Experiencia(BaseModel):
    empresa: str
    cargo: str
    anioInicio: str
    anioFin: str  

class Idioma(BaseModel):
    idioma: str
    nivel: str
    
class OfertaDeTrabajo(BaseModel):
    empresa: str
    descripcion: str
    
class FormDataModel(BaseModel):
    datosPersonales: DatosPersonales
    educacion: list[Educacion]
    certificaciones: list[Certificacion]
    experiencia: list[Experiencia]
    idiomas: list[Idioma]
    foto: bool
    ofertaDeTrabajo: OfertaDeTrabajo

