import os, platform, json
sistema = platform.system()
if(sistema =="Linux"):
    from funcionConsultasBD import ejecutarSQLlocal as ejecutarConsultaSQL
    from resourceManager import execLocal as execCommand
else:
    from funcionConsultasBD import ejecutarSQLRemoto as ejecutarConsultaSQL
    from resourceManager import execRemoto as execCommand

def crearSliceBD(data, idUser, idOpenstack="", idLinux=""):
    try:
        plataformaDespliegue = data['AZ']
        azs = ["Golden Zone", "Silver Zone"]
        if(plataformaDespliegue == azs[0]):
            ejecutarConsultaSQL("INSERT INTO slice (nombre, idOpenstackproject, idLinuxproject, usuario_idUsuario, fecha, sliceJSON) VALUES (%s, %s, %s, %s, %s, %s)",
                                (data['nombre'], idOpenstack, "", idUser, data['fecha'], json.dumps(data)))
            result = ejecutarConsultaSQL("SELECT idSlice from slice where idOpenstackproject=%s ",(idOpenstack,) )
        else:
            ejecutarConsultaSQL("INSERT INTO slice (nombre, idOpenstackproject, idLinuxproject, usuario_idUsuario, fecha, sliceJSON) VALUES (%s, %s, %s, %s, %s, %s)",
                                (data['nombre'], "", idLinux, idUser, data['fecha'], json.dumps(data)))
            result = ejecutarConsultaSQL("SELECT idSlice from slice where idLinuxproject=%s ",(idLinux,) )
        return result[0]
    except Exception as e:
        return e

def modificarSlice(data):
    pass