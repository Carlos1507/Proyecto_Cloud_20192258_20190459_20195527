from typing import Optional, List, Union
from pydantic import BaseModel, validator, ValidationError

class Usuario(BaseModel):
    idUsuario: Optional[int] = None
    username: str
    passwd: str
    email: str
    Roles_idRoles: int
class Flavor(BaseModel):
    idflavors: Optional[int] = None
    ram_mb: int
    disk_gb: int
    cpus: int
    nombre: str
    idflavorglance: Optional[str] = None
class Recursos(BaseModel):
    idRecursos: Optional[int] = None
    worker: Optional[str]
    memoriaUso: Optional[int]
    memoriaTotal: Optional[int]
    discoAsignado: Optional[int]
    discoTotal: Optional[int]
    cpusAsignado: Optional[int]
    cpuTotal: Optional[int]
class UserValidation(BaseModel):
    username: str
    password: str
class Email(BaseModel):
    title: str
    email: str
    username: str
    password: str
class Imagen(BaseModel):
    nombre: str
    filename: Optional[str] = None
    idglance: Optional[str] = None
    VMs_idRecursos: Optional[int] = None
class Slice(BaseModel):
    idSlice: Optional[int] = None
    nombre: Optional[str]
    idOpenstackproject: Optional[str] = None
    idLinuxproject: Optional[str] = None
    usuario_idUsuario: Optional[int]
    fecha: Optional[str] =  None
    sliceJSON: str

