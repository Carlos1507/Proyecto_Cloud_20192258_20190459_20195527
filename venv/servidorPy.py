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
    return handlermysql.fetchall()

class Usuario(BaseModel):
    idUsuario: int
    username: str
    passwd: str
    email: Optional[float] = None
    flagAZ: Optional[bool] = None
    Roles_idRoles: Optional[str]

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
    print("Contraseña a validar: ", uservalid.password)
    result = ejecutarConsultaSQL("SELECT * FROM usuario where (username= %s and passwd= %s)", (uservalid.username, uservalid.password))
    if (len(result)!=0):
        return {"result": result[0]}
    else:
        return {"result":"Incorrecto"}