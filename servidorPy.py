#!/usr/bin/python
from fastapi import FastAPI, Request
from typing import Optional
from pydantic import BaseModel
import random, platform
from resourceManager import validarRecursosDisponibles
from vmPlacement import crearSlice

sistema = platform.system()
if(sistema =="Linux"):
    from Recursos.funcionConsultasBD import ejecutarSQLlocal as ejecutarConsultaSQL
else:
    from Recursos.funcionConsultasBD import ejecutarSQLRemoto as ejecutarConsultaSQL


listaSlicesGeneral = [["Prueba", "11/07/2023", "4", "5", "Si"],
                      ["VNRT","7/04/2023","10","20","Si"],
                      ["Exogeni","2/01/2023","15","20","Si"],
                      ["Entorno1", "19/07/2023", "8", "9", "No"],
                      ["Simulación", "4/08/2023", "6", "10", "Si"]]

class Usuario(BaseModel):
    idUsuario: Optional[int] = None
    username: str
    passwd: str
    email: str
    flagAZ: bool
    Roles_idRoles: int

class UserValidation(BaseModel):
    username: str
    password: str

class Imagen(BaseModel):
    nombre: str
    VMs_idRecursos: Optional[int] = None
class AZsConf(BaseModel):
    azs: list

app = FastAPI()

plataformaEnUso = ""
disponible = True
contClientes = 0
usuarioEnAtencion = 0

@app.get("/")
async def hello():
    return {"result":"hello world from remote node"}

@app.get("/disponible/{idUser}")
async def disponibleValidar(idUser: int):
    global disponible, contClientes, usuarioEnAtencion
    if(disponible == True & contClientes == 0):
        disponible == False
        contClientes +=1
        usuarioEnAtencion = idUser
        return {"result":"Disponible"}
    else:
        return {"result":"Ocupado"}

@app.post("/validacionRecursos/{idUser}")
async def validacionRecursosDisponibles(idUser: int, request: Request):
    global usuarioEnAtencion, disponible, contClientes
    if(usuarioEnAtencion == idUser):
        data = await request.json()
        if(validarRecursosDisponibles(data) == True): ## Resource Manager
            crearSlice(data)   ## VM Placement
            return {"result": "Slice creado exitosamente"}
        else:
            return {"result": "En este momentoNo se cuentan con los suficientes \
                    recursos para generar este slice"}
    else:
        return {"result":"El servidor está atentiendo a otro usuario, espere su turno"}

@app.get("/allUsers/remoto")
async def allUsersRemoto():
    result = ejecutarConsultaSQL("SELECT idUsuario, username, email, flagAZ, Roles_idRoles FROM usuario", ())
    listaUsuarios = [list(tupla) for tupla in result]
    return {"result": listaUsuarios}

@app.post("/items/create")
async def create_item(item: Usuario):
    return {"item_id": item.name, **item.dict()}

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
    
@app.get("/allUsers")
async def allUsers():
    result = ejecutarConsultaSQL("SELECT idUsuario, username, email, flagAZ, Roles_idRoles FROM usuario", ())
    listaUsuarios = [list(tupla) for tupla in result]
    return {"result": listaUsuarios}

@app.get("/allSlices")
async def allSlices():
    return {"result": listaSlicesGeneral}

@app.get("/slicesUser/{idUser}")
async def allSlicesUser(idUser: int):
    num_slices = random.randint(1, len(listaSlicesGeneral))
    slicesUser = random.sample(listaSlicesGeneral, num_slices)
    return {"result": slicesUser}

@app.get("/eliminarUsuario/{idUser}")
async def eliminarUsuarios(idUser: int):
    try:
        ejecutarConsultaSQL("DELETE FROM usuario WHERE idUsuario = %s", (idUser,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

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
        ejecutarConsultaSQL("INSERT INTO imagenes (nombre) VALUES (%s)", (imagen.nombre,))
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