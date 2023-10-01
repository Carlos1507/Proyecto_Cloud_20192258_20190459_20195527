#!/usr/bin/python
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import pymysql

def ejecutarConsultaSQL(sql, params):
    mysqlConexion = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="cloud", charset="utf8mb4")
    handlermysql = mysqlConexion.cursor()
    handlermysql.execute(sql, params)
    mysqlConexion.close()
    resultados = handlermysql.fetchall()
    return resultados
def ejecutarSQLNoSelect(sql, params):
    try:
        mysqlConexion = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="cloud", charset="utf8mb4")
        handlermysql = mysqlConexion.cursor()
        if params is not None:
            handlermysql.execute(sql, params)
        else:
            handlermysql.execute(sql)
        mysqlConexion.commit()
        mysqlConexion.close()
        print("Cambio exitoso")
    except pymysql.Error as e:
        print("Error al realizar el cambio:", e)

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

app = FastAPI()

@app.get('/')
async def root():
    return {"menssage":"Hello world"}   

@app.get("/items/{item_id}")
async def items(item_id: int):
    return {"item_id":item_id}

@app.post("/items/create")
async def create_item(item: Usuario):
    return {"item_id": item.name, **item.dict()}

@app.post("/validarPOST")
async def validate_password(uservalid: UserValidation):
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

@app.get("/eliminarUsuario/{idUser}")
async def eliminarUsuarios(idUser: int):
    try:
        ejecutarSQLNoSelect("DELETE FROM usuario WHERE idUsuario = %s", (idUser,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

@app.post("/crearUsuario")
async def crearUsuario(user: Usuario):
    try:
        print(user.Roles_idRoles, "tipo: ",type(user.Roles_idRoles))
        ejecutarSQLNoSelect("INSERT INTO usuario (username, passwd, email, flagAZ, Roles_idRoles) VALUES (%s, %s, %s, %s, %s)",
                            (user.username,user.passwd,user.email,0,user.Roles_idRoles))
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}