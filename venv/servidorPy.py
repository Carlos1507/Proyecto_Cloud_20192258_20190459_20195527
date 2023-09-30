#!/usr/bin/python
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import bcrypt
import pymysql


# Lado del cliente
def hash_bcrypt(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password
def comprobar_hash_bcrypt(input_passwd, password_hashed):
    if bcrypt.checkpw(input_passwd, password_hashed):
        print("Contraseña correcta")
    else:
        print("Contraseña incorrectaaaaaa")
def validar(uservalid):
    mysqlConexion = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="happyhierba", charset="utf8mb4")
    handlermysql = mysqlConexion.cursor()
    sql = "SELECT * FROM happyhierba.persona where (username= %s and contrasenia= %s)"
    handlermysql.execute(sql, (uservalid.username, uservalid.password))
    print(handlermysql.fetchall())
    mysqlConexion.close()


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

@app.get("/passwd/{contrasenia}")
async def passwordEncoder(contrasenia:str):
    return {"contrasenia_hash": hash_bcrypt(contrasenia)}

@app.post("/validarPOST")
async def validate_password(uservalid: UserValidation):
    print(uservalid)
    validar(uservalid)
    return {"result":"hello"}
