#!/usr/bin/python
from fastapi import FastAPI, Request
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import random, platform, json, os, uvicorn
from resourceManager import validarRecursosDisponibles
from vmPlacement import crearSlice
from vmPlacement import modificarSlice

app = FastAPI()

sistema = platform.system()
if(sistema =="Linux"):
    from funcionConsultasBD import ejecutarSQLlocal as ejecutarConsultaSQL
else:
    from funcionConsultasBD import ejecutarSQLRemoto as ejecutarConsultaSQL

class Usuario(BaseModel):
    idUsuario: Optional[int] = None
    username: str
    passwd: str
    email: str
    flagAZ: bool
    Roles_idRoles: int

class Flavor(BaseModel):
    idflavors: Optional[int] = None
    ram_mb: float
    disk_gb: float
    cpus: int
    nombre: str
    idflavorglance: Optional[str] = None

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

class UserValidation(BaseModel):
    username: str
    password: str

class Imagen(BaseModel):
    nombre: str
    filename: Optional[str] = None
    idglance: Optional[str] = None
    VMs_idRecursos: Optional[int] = None

class AZsConf(BaseModel):
    azs: list

app = FastAPI()

plataformaEnUso = ""
slicesUsuarios = [{3: {'vms': [{'nombre': 'vm1', 'capacidad': '1024', 'cpu': '2', 'imagen': 'cirros.img'}, {'nombre': 'vm2', 'capacidad': '1024', 'cpu': '2', 'imagen': 'cirros.img'}, {'nombre': 'vm3', 'capacidad': '1024', 'cpu': '2', 'imagen': 'cirros.img'}, {'nombre': 'vm4', 'capacidad': '1024', 'cpu': '2', 'imagen': 'cirros.img'}], 'enlaces': [['vm4', 'vm1'], ['vm1', 'vm3'], ['vm2', 'vm1']], 'nombre': 'Prueba', 'fecha': '09/10/2023'}}]  
disponible = True
usuarioEnAtencion = 0

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
    global usuarioEnAtencion, disponible, slicesUsuarios
    if(usuarioEnAtencion == idUser):
        data = await request.json()
        if(validarRecursosDisponibles(data) == True): ## Resource Manager
            crearSlice(data)   ## VM Placement
            listaSlices = slicesUsuarios
            listaSlices.append({idUser: data})
            slicesUsuarios = listaSlices
            disponible = True
            print(slicesUsuarios)
            return {"result": "Slice creado exitosamente"}
        else:
            return {"result": "En este momentoNo se cuentan con los suficientes \
                    recursos para generar este slice"}
    else:
        return {"result":"El servidor está atentiendo a otro usuario, espere su turno"}
    
async def allUsersRemoto():
    result = ejecutarConsultaSQL("SELECT idUsuario, username, email, flagAZ, Roles_idRoles FROM usuario", ())
    listaUsuarios = [list(tupla) for tupla in result]
    return {"result": listaUsuarios}

@app.post("/validarPOST")
async def validate_password(uservalid: UserValidation):
    global plataformaEnUso
    print("Plataforma "+plataformaEnUso)
    result = ejecutarConsultaSQL("SELECT * FROM usuario where (username= %s and passwd= %s)", (uservalid.username, uservalid.password))
    print(type(result), result)
    if (len(result)!=0):
        return {"result": result[0]}
    else:
        return {"result":"Incorrecto"}
    
@app.post("/saveFlavor")
async def saveFlavor(flavor: Flavor):
    try:
        result = ejecutarConsultaSQL("INSERT INTO flavors (ram_mb, disk_gb, cpus, nombre, idflavorglance) VALUES (%s, %s, %s, %s, %s)",
                            (flavor.ram_mb, flavor.disk_gb, flavor.cpus, flavor.nombre, flavor.idflavorglance))
        
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}

@app.get("/allUsers")
async def allUsers():
    result = ejecutarConsultaSQL("SELECT idUsuario, username, email, flagAZ, Roles_idRoles FROM usuario", ())
    listaUsuarios = [list(tupla) for tupla in result]
    return {"result": listaUsuarios}

@app.get("/allSlices")
async def allSlices():
    global slicesUsuarios
    return {"result": slicesUsuarios}

@app.get("/slicesUser/{idUser}")
async def allSlicesUser(idUser: int):
    global slicesUsuarios
    slicesUser = [diccionario for diccionario in slicesUsuarios if idUser in diccionario]
    return {"result": slicesUser}

@app.get("/eliminarUsuario/{idUser}")
async def eliminarUsuarios(idUser: int):
    try:
        ejecutarConsultaSQL("DELETE FROM usuario WHERE idUsuario = %s", (idUser,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}
    
@app.post("/eliminarSlice/{idUser}")
async def eliminarSlice(idUser: str, request: Request):
    global slicesUsuarios
    data = await request.json()
    print(json.dumps(data))

    listaSlicesUsuariosModif = slicesUsuarios
    print(data[idUser]['nombre'])

    for slice in slicesUsuarios:
        idUsuario = next(iter(slice.keys()))
        nombre = slice[idUsuario]['nombre']
        if(nombre ==data[idUser]['nombre']):
            sliceEliminar = slice
    listaSlicesUsuariosModif.remove(sliceEliminar)
    slicesUsuarios = listaSlicesUsuariosModif
    return {"result":"Eliminado con éxito"}

@app.post("/changeSlice/{idUser}")
async def validacionRecursosDisponibles(idUser: int, request: Request):
    data = await request.json()
    if(validarRecursosDisponibles(data) == True): ## Resource Manager
        modificarSlice(data)   ## VM Placement
        return {"result": "Slice creado exitosamente"}
    else:
        return {"result": "En este momentoNo se cuentan con los suficientes "+ \
                 "recursos para generar este slice"}

@app.post("/crearUsuario")
async def crearUsuario(user: Usuario):
    try:
        print(user.Roles_idRoles, "tipo: ",type(user.Roles_idRoles))
        ejecutarConsultaSQL("INSERT INTO usuario (username, passwd, email, flagAZ, Roles_idRoles) VALUES (%s, %s, %s, %s, %s)",
                            (user.username,user.passwd,user.email,0,user.Roles_idRoles))
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
    
@app.get("/allImagenes")
async def listarImagenes():
    result = ejecutarConsultaSQL("SELECT idImagenes, nombre FROM imagenes", ())
    listaImagenes = [list(tupla) for tupla in result]
    return {"result": listaImagenes}

@app.get("/allFlavors")
async def listarFlavors():
    result = ejecutarConsultaSQL("SELECT * FROM flavors", ())
    listaFlavors = []
    for elem in result:
        print(elem)
        listaFlavors.append(FlavorBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
    return {"result": listaFlavors}

@app.get("/eliminarFlavor/{idFlavor}")
async def eliminarFlavor(idFlavor: int):
    try:
        ejecutarConsultaSQL("DELETE FROM flavors WHERE idflavors = %s", (idFlavor,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

@app.get("/eliminarImagen/{idImagen}")
async def eliminarImagen(idImagen: str):
    try:
        ejecutarConsultaSQL("DELETE FROM imagenes WHERE idImagenes = %s", (idImagen,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}
    
@app.post("/agregarImagen")
async def agregarImagen(imagen: Imagen):
    print(imagen)
    try:
        ejecutarConsultaSQL("INSERT INTO imagenes (nombre, filename, idglance) VALUES (%s, %s, %s)", (imagen.nombre,imagen.filename, imagen.idglance))  
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

@app.post("/guardarAZs")
async def guardarAZs(confAZ: AZsConf):
    print("Helloooooooo")
    ejecutarConsultaSQL("DELETE FROM zonas",())
    ejecutarConsultaSQL("ALTER TABLE zonas AUTO_INCREMENT = 1",())
    for az in confAZ.azs:
        ejecutarConsultaSQL("INSERT INTO zonas (nombre) values (%s)", az)

@app.get("/guardarPlataforma/{plataforma}")
async def guardarPlataforma(plataforma: str):
    print(plataforma)
    global plataformaEnUso
    plataformaEnUso = plataforma
    return {"result":"Guardado exitoso"}

if __name__ == "__main__":
    uvicorn.run("servidorPy:app", host="0.0.0.0", port=8000, reload=True)