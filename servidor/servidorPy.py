#!/usr/bin/python
from fastapi import FastAPI, Request
from typing import Optional, List, Union
from pydantic import BaseModel, validator, ValidationError
from fastapi.responses import HTMLResponse
import platform, os, uvicorn, json, ast
from resourceManager import validarRecursosDisponibles
from vmPlacement import crearSlice
from vmPlacement import modificarSlice

app = FastAPI()

sistema = platform.system()
if(sistema =="Linux"):
    from funcionConsultasBD import ejecutarSQLlocal as ejecutarConsultaSQL
else:
    from funcionConsultasBD import ejecutarSQLRemoto as ejecutarConsultaSQL

#####################################################################
########################## MODELADOS ################################
#####################################################################

####################### MODELOS CONSULTAS ###########################
class Usuario(BaseModel):
    idUsuario: Optional[int] = None
    username: str
    passwd: str
    email: str
    Roles_idRoles: int
class Flavor(BaseModel):
    idflavors: Optional[int] = None
    ram_mb: float
    disk_gb: float
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

########################### MODELOS BD ##############################
class FlavorBD:
    def __init__(self, idflavors, ram_mb, disk_gb, cpus, nombre, idflavorglance):
        self.nombre = nombre
        self.ram = ram_mb
        self.cpu = cpus
        self.disk = disk_gb
        self.idflavors = idflavors
        self.idflavorglance = idflavorglance
    def to_dict(self):
        return {
            'idflavors': self.idflavors,
            'ram_mb': self.ram,
            'disk_gb': self.disk, 
            'cpus': self.cpu,
            'nombre': self.nombre,
            'idflavorglace': self.idflavorglance
        }
class RecursosBD:
    def __init__(self, idRecursos, worker, memoriaUso, memoriaTotal, discoAsignado, discoTotal, cpusAsignado, cpuTotal):
        self.idRecursos = idRecursos
        self.worker = worker
        self.memoriaUso = memoriaUso
        self.memoriaTotal = memoriaTotal
        self.discoAsignado = discoAsignado
        self.discoTotal = discoTotal
        self.cpusAsignado = cpusAsignado
        self.cpuTotal = cpuTotal
    def to_dict(self):
        return {
            'idRecursos': self.idRecursos,
            'worker': self.worker,
            'memoriaUso': self.memoriaUso, 
            'memoriaTotal': self.memoriaTotal,
            'discoAsignado': self.discoAsignado,
            'discoTotal': self.discoTotal,
            'cpusAsignado': self.cpusAsignado,
            'cpuTotal': self.cpuTotal
        }
class SliceBD:
    def __init__(self, idSlice, nombre, idOpenstackproject, idLinuxproject, usuario_idUsuario, fecha, sliceJSON):
        self.idSlice = idSlice
        self.nombre = nombre
        self.idOpenstackproject = idOpenstackproject
        self.idLinuxproject = idLinuxproject
        self.usuario_idUsuario = usuario_idUsuario
        self.fecha = fecha
        self.sliceJSON = sliceJSON
    def to_dict(self):
        return {
            'idSlice': self.idSlice,
            'nombre': self.nombre,
            'idOpenstackproject': self.idOpenstackproject, 
            'idLinuxproject': self.idLinuxproject,
            'usuario_idUsuario': self.usuario_idUsuario,
            'fecha': self.fecha,
            'sliceJSON': self.sliceJSON
        }
class ImagenBD:
    def __init__(self, idImagenes, nombre, filename, idglance):
        self.idImagenes = idImagenes
        self.nombre = nombre
        self.filename = filename
        self.idglance = idglance
    def to_dict(self):
        return {
            'idImagenes': self.idImagenes,
            'nombre': self.nombre,
            'filename': self.filename, 
            'idglance': self.idglance
        }

disponible = True
usuarioEnAtencion = 0

#####################################################################
########################## ENDPOINTS ################################
#####################################################################

######################### GENERALES #############################
@app.get("/")
async def hello():
    global slicesUsuarios
    print(slicesUsuarios)
    return {"result":"hello world from remote node"}
@app.get("/log")
async def log():
    try:
        filename = "salida.log"
        if os.path.exists(filename):
            with open(filename, "r") as archivo:
                contenido = archivo.read()
                contenido_html = contenido.replace("\n", "<br>")
            return HTMLResponse(content=contenido_html)
        else:
            return HTMLResponse(content="<p>El archivo no se encontró</p>", status_code=404)
    except FileNotFoundError:
        return HTMLResponse(content="<p>El archivo no se encontró</p>", status_code=404)
    except IOError:
        return HTMLResponse(content="<p>Ocurrió un error al intentar abrir el archivo</p>", status_code=500)

########################## USUARIO ##############################
@app.post("/usuario/validar")
async def usuarioValidar(uservalid: UserValidation):
    result = ejecutarConsultaSQL("SELECT * FROM usuario where (username= %s and passwd= %s)", (uservalid.username, uservalid.password))
    print(type(result), result)
    if (len(result)!=0):
        return {"result": result[0]}
    else:
        return {"result":"Incorrecto"}
@app.get("/usuario/listar")
async def usuarioListar():
    result = ejecutarConsultaSQL("SELECT idUsuario, username, email, Roles_idRoles FROM usuario", ())
    listaUsuarios = [list(tupla) for tupla in result]
    return {"result": listaUsuarios}
@app.post("/usuario/crear")
async def usuarioCrear(user: Usuario):
    try:
        print(user.Roles_idRoles, "tipo: ",type(user.Roles_idRoles))
        ejecutarConsultaSQL("INSERT INTO usuario (username, passwd, email, Roles_idRoles) VALUES (%s, %s, %s, %s)",
                            (user.username,user.passwd,user.email,0,user.Roles_idRoles))
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
@app.get("/usuario/eliminar/{idUser}")
async def usuarioEliminar(idUser: int):
    try:
        ejecutarConsultaSQL("DELETE FROM usuario WHERE idUsuario = %s", (idUser,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

########################## IMAGENES ##############################
@app.get("/imagenes/listar")
async def imagenesListar():
    result = ejecutarConsultaSQL("SELECT * FROM imagenes", ())
    listaImagenes = []
    for elem in result:
        print(elem)
        listaImagenes.append(ImagenBD(elem[0], elem[1], elem[2], elem[3]))
    return {"result": listaImagenes}
@app.get("/imagen/eliminar/{idImagen}")
async def imagenesEliminar(idImagen: str):
    try:
        ejecutarConsultaSQL("DELETE FROM imagenes WHERE idImagenes = %s", (idImagen,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}
@app.post("/imagen/crear")
async def imagenesCrear(imagen: Imagen):
    print(imagen)
    try:
        ejecutarConsultaSQL("INSERT INTO imagenes (nombre, filename, idglance) VALUES (%s, %s, %s)", (imagen.nombre,imagen.filename, imagen.idglance))  
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

########################## FLAVORS ##############################
@app.get("/flavors/listar")  # allFlavors
async def flavorsListar():
    result = ejecutarConsultaSQL("SELECT * FROM flavors", ())
    listaFlavors = []
    for elem in result:
        print(elem)
        listaFlavors.append(FlavorBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
    return {"result": listaFlavors}
@app.get("/flavors/eliminar/{idFlavor}")   # eliminarFlavor
async def flavorsEliminar(idFlavor: int):
    try:
        ejecutarConsultaSQL("DELETE FROM flavors WHERE idflavors = %s", (idFlavor,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}
@app.post("/flavors/crear")
async def flavorsCrear(flavor: Flavor):
    try:
        result = ejecutarConsultaSQL("INSERT INTO flavors (ram_mb, disk_gb, cpus, nombre, idflavorglance) VALUES (%s, %s, %s, %s, %s)",
                            (flavor.ram_mb, flavor.disk_gb, flavor.cpus, flavor.nombre, flavor.idflavorglance))
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
    
########################## RECURSOS ##############################
@app.post("/recursos/crear")
async def recursosCrear(recurso: Recursos):
    try:
        result = ejecutarConsultaSQL("INSERT INTO recursos (worker, memoriaUso, memoriaTotal, discoAsignado, discoTotal, cpusAsignado, cpuTotal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (recurso.worker, recurso.memoriaUso, recurso.memoriaTotal, recurso.discoAsignado, recurso.discoTotal, recurso.cpusAsignado, recurso.cpuTotal))
        return {"result":result}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
@app.get("/recursos/listar")
async def recursosListar():
    result = ejecutarConsultaSQL("SELECT * FROM recursos", ())
    listaRecursos = []
    for elem in result:
        print(elem)
        listaRecursos.append(RecursosBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))
    return {"result": listaRecursos}
@app.post("/recursos/actualizar")
async def recursosActualizar(recurso: Recursos):
    try:
        result = ejecutarConsultaSQL("UPDATE recursos SET worker = %s, memoriaUso = %s, memoriaTotal=%s, discoAsignado=%s, discoTotal=%s, cpusAsignado=%s, cpuTotal=%s where idRecursos = %s",
                            (recurso.worker, recurso.memoriaUso, recurso.memoriaTotal, recurso.discoAsignado, recurso.discoTotal, recurso.cpusAsignado, recurso.cpuTotal, recurso.idRecursos))
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
@app.get("/recursos/eliminar/{idRecursos}")
async def recursosEliminar(idRecursos: int):
    try:
        ejecutarConsultaSQL("DELETE FROM recursos WHERE idRecursos = %s", (idRecursos,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

########################### SLICES  ANTIGUO ###############################
@app.get("/slice/listarPorUsuario/{idUser}")
async def allSlicesUser(idUser: int):
    result = ejecutarConsultaSQL("SELECT * FROM slice where usuario_idUsuario = %s", (idUser,))
    listaSlices = []
    if(len(result)==0):
        return {"result":[]}
    else:
        for elem in result:
            listaSlices.append(SliceBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], json.loads(elem[6])).to_dict())
        return {"result": listaSlices}

@app.post("/eliminarSlice/{idUser}")
async def eliminarSlice(idUser: str, request: Request):
    global slicesUsuarios
    data = await request.json()
    listaSlicesUsuariosModif = slicesUsuarios
    for slice in slicesUsuarios:
        idUsuario = next(iter(slice.keys()))
        nombre = slice[idUsuario]['nombre']
        if(nombre ==data[idUser]['nombre']):
            sliceEliminar = slice
    listaSlicesUsuariosModif.remove(sliceEliminar)
    slicesUsuarios = listaSlicesUsuariosModif
    return {"result":"Eliminado con éxito"}

########################### SLICES NUEVO ###############################
@app.get("/slice/listar")
async def sliceListar():
    result = ejecutarConsultaSQL("SELECT idSlice, nombre, idOpenstackproject, idLinuxProject, usuario_idUsuario, fecha, sliceJSON, username FROM slice INNER JOIN usuario ON slice.usuario_idUsuario = usuario.idUsuario", ())
    listaSlices = []
    if(len(result)==0):
        return {"result":[]}
    else:
        for elem in result:
            listaSlices.append({"user": elem[7] , "slice":SliceBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], json.loads(elem[6])).to_dict()})
        return {"result": listaSlices}

########################### RESOURCE MANAGER & VM PLACEMENT ###############################
@app.get("/disponible/{idUser}")
async def disponibleValidar(idUser: int):
    global disponible, usuarioEnAtencion
    if(disponible == True):
        print("Disponible")
        disponible == False
        usuarioEnAtencion = idUser
        return {"result":"Disponible"}
    else:
        print("Ocupado")
        return {"result":"Ocupado"}
@app.post("/validacionRecursos/{idUser}")
async def validacionRecursosDisponibles(idUser: int, request: Request):
    global usuarioEnAtencion, disponible
    if(usuarioEnAtencion == idUser):
        data = await request.json()
        if(validarRecursosDisponibles(data) == True): ## Resource Manager
            crearSlice(data, idUser)   ## VM Placement
            disponible = True
            return {"result": "Slice creado exitosamente"}
        else:
            return {"result": "En este momentoNo se cuentan con los suficientes \
                    recursos para generar este slice"}
    else:
        return {"result":"El servidor está atentiendo a otro usuario, espere su turno"}

 

########################## INICIALIZACIÓN ##############################
if __name__ == "__main__":
    uvicorn.run("servidorPy:app", host="0.0.0.0", port=8000, reload=True)