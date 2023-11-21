#!/usr/bin/python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import platform, os, uvicorn, json, ast
from resourceManager import validarRecursosDisponibles, consultarRecursosBD, obtenerIDOpenstackProject, actualizarRecursosDisponibles, crearVM_BD
from vmPlacement import crearSliceBD
from vmPlacement import modificarSlice
from modelosBD import *
from modelosConsultas import *
import funcionEnviarMail as send
import slice_creation_openstack as openstackFeatures
import slice_creation_linux as linuxFeatures

app = FastAPI()

sistema = platform.system()
if(sistema =="Linux"):
    from funcionConsultasBD import ejecutarSQLlocal as ejecutarConsultaSQL
    from resourceManager import execLocal as execCommand
    ipOpenstack = "127.0.0.1"
else:
    from funcionConsultasBD import ejecutarSQLRemoto as ejecutarConsultaSQL
    from resourceManager import execRemoto as execCommand
    ipOpenstack = "10.20.10.221"
disponible = True
usuarioEnAtencion = 0

#####################################################################
########################## ENDPOINTS ################################
#####################################################################

######################### GENERALES #############################
@app.get("/", tags=["Conexión exitosa"])
async def hello():
    return {"result":"hello world from other node"}
@app.get("/log", tags=["Log"])
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

########################## USUARIO #############################
@app.post("/usuario/validar", tags=["Usuario"])
async def usuarioValidar(uservalid: UserValidation):
    result = ejecutarConsultaSQL("SELECT * FROM usuario where (username= %s and passwd= %s)", (uservalid.username, uservalid.password))
    print(type(result), result)
    if (len(result)!=0):
        return {"result": result[0]}
    else:
        return {"result":"Incorrecto"}
@app.get("/usuario/listar", tags=["Usuario"])
async def usuarioListar():
    result = ejecutarConsultaSQL("SELECT idUsuario, username, email, Roles_idRoles FROM usuario", ())
    listaUsuarios = [list(tupla) for tupla in result]
    return {"result": listaUsuarios}
@app.post("/usuario/crear", tags=["Usuario"])
async def usuarioCrear(user: Usuario):
    try:
        print(user.Roles_idRoles, "tipo: ",type(user.Roles_idRoles))
        ejecutarConsultaSQL("INSERT INTO usuario (username, passwd, email, Roles_idRoles) VALUES (%s, %s, %s, %s)",
                            (user.username,user.passwd,user.email,user.Roles_idRoles))
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
@app.delete("/usuario/eliminar/{idUser}", tags=["Usuario"])
async def usuarioEliminar(idUser: int):
    try:
        username = ejecutarConsultaSQL("SELECT username FROM usuario where idUsuario = %s", (idUser,))[0]
        execCommand("openstack user delete "+username, "10.20.10.221")
        ejecutarConsultaSQL("DELETE FROM usuario WHERE idUsuario = %s", (idUser,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

########################## IMAGENES ############################
@app.get("/imagenes/listar", tags=["Imágenes"])
async def imagenesListar():
    result = ejecutarConsultaSQL("SELECT * FROM imagenes", ())
    listaImagenes = []
    for elem in result:
        print(elem)
        listaImagenes.append(ImagenBD(elem[0], elem[1], elem[2], elem[3]))
    return {"result": listaImagenes}
@app.delete("/imagen/eliminar/{idImagen}", tags=["Imágenes"])
async def imagenesEliminar(idImagen: str):
    try:
        ejecutarConsultaSQL("DELETE FROM imagenes WHERE idImagenes = %s", (idImagen,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}
@app.post("/imagen/crear", tags=["Imágenes"])
async def imagenesCrear(imagen: Imagen):
    print(imagen)
    try:
        ejecutarConsultaSQL("INSERT INTO imagenes (nombre, filename, idglance) VALUES (%s, %s, %s)", (imagen.nombre,imagen.filename, imagen.idglance))  
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

########################## FLAVORS #############################
@app.get("/flavors/listar", tags=["Flavors"])  # allFlavors
async def flavorsListar():
    result = ejecutarConsultaSQL("SELECT * FROM flavors", ())
    listaFlavors = []
    for elem in result:
        print(elem)
        listaFlavors.append(FlavorBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
    return {"result": listaFlavors}
@app.delete("/flavors/eliminar/{idFlavor}", tags=["Flavors"])   # eliminarFlavor
async def flavorsEliminar(idFlavor: int):
    try:
        ejecutarConsultaSQL("DELETE FROM flavors WHERE idflavors = %s", (idFlavor,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}
@app.post("/flavors/crear", tags=["Flavors"])
async def flavorsCrear(flavor: Flavor):
    try:
        result = ejecutarConsultaSQL("INSERT INTO flavors (ram_mb, disk_gb, cpus, nombre, idflavorglance) VALUES (%s, %s, %s, %s, %s)",
                            (flavor.ram_mb, flavor.disk_gb, flavor.cpus, flavor.nombre, flavor.idflavorglance))
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
    
########################## RECURSOS ############################
@app.post("/recursos/crear", tags=["Recursos"])
async def recursosCrear(recurso: Recursos):
    try:
        result = ejecutarConsultaSQL("INSERT INTO recursos (worker, memoriaUso, memoriaTotal, discoAsignado, discoTotal, cpusAsignado, cpuTotal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (recurso.worker, recurso.memoriaUso, recurso.memoriaTotal, recurso.discoAsignado, recurso.discoTotal, recurso.cpusAsignado, recurso.cpuTotal))
        return {"result":result}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
@app.get("/recursos/listar", tags=["Recursos"])
async def recursosListar():
    listaRecursos = consultarRecursosBD()
    return {"result": listaRecursos}
@app.put("/recursos/actualizar", tags=["Recursos"])
async def recursosActualizar(recurso: Recursos):
    try:
        result = ejecutarConsultaSQL("UPDATE recursos SET worker = %s, memoriaUso = %s, memoriaTotal=%s, discoAsignado=%s, discoTotal=%s, cpusAsignado=%s, cpuTotal=%s where idRecursos = %s",
                            (recurso.worker, recurso.memoriaUso, recurso.memoriaTotal, recurso.discoAsignado, recurso.discoTotal, recurso.cpusAsignado, recurso.cpuTotal, recurso.idRecursos))
        return {"result":"Correcto"}
    except Exception as e:
        print("Error: ", e)
        return {"result":"Error"}
@app.delete("/recursos/eliminar/{idRecursos}", tags=["Recursos"])
async def recursosEliminar(idRecursos: int):
    try:
        ejecutarConsultaSQL("DELETE FROM recursos WHERE idRecursos = %s", (idRecursos,))
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}

########################## SLICES #############################
@app.get("/slice/listar", tags=["Slices"])
async def sliceListar():
    result = ejecutarConsultaSQL("SELECT idSlice, nombre, idOpenstackproject, idLinuxProject, usuario_idUsuario, fecha, sliceJSON, username FROM slice INNER JOIN usuario ON slice.usuario_idUsuario = usuario.idUsuario", ())
    listaSlices = []
    if(len(result)==0):
        return {"result":[]}
    else:
        for elem in result:
            listaSlices.append({"user": elem[7] , "slice":SliceBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], json.loads(elem[6])).to_dict()})
        return {"result": listaSlices}
@app.get("/slice/listarPorUsuario/{idUser}", tags=["Slices"])
async def sliceListarPorUsuario(idUser: int):
    result = ejecutarConsultaSQL("SELECT * FROM slice where usuario_idUsuario = %s", (idUser,))
    listaSlices = []
    if(len(result)==0):
        return {"result":[]}
    else:
        for elem in result:
            listaSlices.append(SliceBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], json.loads(elem[6])).to_dict())
        return {"result": listaSlices}
@app.delete("/slice/eliminar/{idUser}/{idSlice}/{nombre}", tags=["Slices"])
async def sliceEliminar(idUser: int, idSlice:int, nombre:str):
    try:
        openstackFeatures.borrarSlice(nombre, ipOpenstack)        
        idVMsBD = ejecutarConsultaSQL("SELECT idvm from vm where slice_idSlice = %s",(idSlice,))
        print("Eliminando VMs...")
        for vm in idVMsBD:
            ejecutarConsultaSQL("DELETE FROM vm WHERE idvm= %s", (vm,))
        ejecutarConsultaSQL("DELETE FROM slice WHERE (idSlice= %s and usuario_idUsuario = %s)", (idSlice,idUser))
        actualizarRecursosDisponibles()
        return {"result":"Correcto"}
    except:
        return {"result":"Error"}


######################## ENVÍO CORREO ########################
@app.post("/send_mail", tags=["Funciones especiales"])
async def send_mail(email: Email):
    try:
        send.send_email(email.title, email.email, email.username, email.password)
        return {"result":"Correcto"}
    except Exception as e:
        return {"result":f"Error {e}"}


########################### RESOURCE MANAGER & VM PLACEMENT ###############################
@app.get("/disponible/{idUser}", tags=["RM & VM"])
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
@app.post("/validacionRecursos/{idUser}/{username}/{passwd}/{project_name}", tags=["RM & VM"])
async def validacionRecursosDisponibles(idUser: int, username: str, passwd:str, project_name: str,request: Request):
    global usuarioEnAtencion, disponible
    if(usuarioEnAtencion == idUser):
        data = await request.json()
        if(validarRecursosDisponibles(data)): ## YA IMPLEMENTADO
            plataformaDespliegue = data['AZ']
            azs = ["Golden Zone", "Silver Zone"]
            if(plataformaDespliegue == azs[0]):
                # Crear en Openstack

                result = openstackFeatures.crearSlice(data,username,passwd,project_name, ipOpenstack) ## YA IMPLEMENTADO
            else:
                # Crear en Linux
                result = linuxFeatures(data)  ## FALTA IMPLEMENTAR
            print("resultCREACIÓN", result)
            if(result != None):
                idOpenstack = obtenerIDOpenstackProject(project_name) ## YA IMPLEMENTADO
                print("idOpenstack", idOpenstack)
                idSliceBD = crearSliceBD(data, idUser, idOpenstack)[0]   ## YA IMPLEMENTADO
                print("idSliceBD", idSliceBD)
                disponible = True
                combinarInfoVMs = combinarInfo(result, data, idSliceBD)
                print("Info combinada", combinarInfoVMs)
                for vm in combinarInfoVMs:
                    print("Creando...", vm['nombre'])
                    crearVM_BD(vm) ## YA IMPLEMENTADO
                print("Actualizar recursos")
                actualizarRecursosDisponibles() ## YA IMPLEMENTADO
                print("Recursos actualizados")
                return {"result": "Slice creado exitosamente"}
        else:
            return {"result": "En este momentoNo se cuentan con los suficientes \
                    recursos para generar este slice"}
    else:
        return {"result":"El servidor está atentiendo a otro usuario, espere su turno"}
    

@app.get("/vm/listar/{project_name}", tags=["VM"])
async def vmListar(project_name: str):
    idSlice = ejecutarConsultaSQL("SELECT idSlice from slice where nombre=%s ",(project_name,))[0]
    result = ejecutarConsultaSQL("SELECT * FROM vm where slice_idSlice=%s", (idSlice,))
    listaVMs = []
    for elem in result:
        listaVMs.append(VMBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8]).to_dict())
    return {"result": listaVMs}

def combinarInfo(result, data, idSliceBD):
    lista_final = []

    # Iterar sobre las VMs en el JSON
    for vm_datos in data['vms']:
        nombre_vm = vm_datos['nombre']
        
        # Verificar si la VM está en el diccionario
        if nombre_vm in result:
            # Crear un nuevo diccionario combinando información
            vm_combinada = {
                "nombre": nombre_vm,
                "alias": vm_datos["alias"],
                "ram": vm_datos["ram"],
                "cpu": vm_datos["cpu"],
                "disk": vm_datos["disk"],
                "imagen": vm_datos["imagen"],
                "idOpenstackImagen": vm_datos["idOpenstackImagen"],
                "idOpenstackFlavor": vm_datos["idOpenstackFlavor"],
                "idVM": result[nombre_vm][0],
                "linkAcceso": result[nombre_vm][1],
                "idSliceBD": idSliceBD
        }
        # Agregar el diccionario a la lista final
        lista_final.append(vm_combinada)
    return lista_final

########################## INICIALIZACIÓN ##############################
if __name__ == "__main__":
    uvicorn.run("servidorPy:app", host="0.0.0.0", port=8000, reload=True)
