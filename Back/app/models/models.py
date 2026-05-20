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
    titulo: str
    institucion: str
    mesInicio: str = ''
    anioInicio: str = ''
    mesFin: str = ''
    anioFin: str = ''
    actualidad: bool = False

class Certificacion(BaseModel):
    certificacion: str
    mes: str = ''
    anio: str = ''

class Experiencia(BaseModel):
    cargo: str
    empresa: str
    mesInicio: str = ''
    anioInicio: str = ''
    mesFin: str = ''
    anioFin: str = ''
    actualidad: bool = False

class Idioma(BaseModel):
    idioma: str
    nivel: str
    
class skills(BaseModel):
    skill: list[str]
    
class OfertaDeTrabajo(BaseModel):
    empresa: str
    descripcion: str
    
class FormDataModel(BaseModel):
    datosPersonales: DatosPersonales
    educacion: list[Educacion]
    certificaciones: list[Certificacion]
    experiencia: list[Experiencia]
    idiomas: list[Idioma]
    skills: list[str]
    foto: bool
    ofertaDeTrabajo: OfertaDeTrabajo
    plantilla: str | None


class Usuario(BaseModel):
    nombre: str
    apellidos: str
    email: str
    contrasena: str
    
class UsuarioLogin(BaseModel):
    email: str
    contrasena: str

class UsuarioRegistro(BaseModel):
    nombre: str
    apellidos: str
    email: str
    contrasena: str