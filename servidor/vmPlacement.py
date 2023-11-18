import os, platform, json
sistema = platform.system()
if(sistema =="Linux"):
    from funcionConsultasBD import ejecutarSQLlocal as ejecutarConsultaSQL
    from resourceManager import execLocal as execCommand
else:
    from funcionConsultasBD import ejecutarSQLRemoto as ejecutarConsultaSQL
    from resourceManager import execRemoto as execCommand

def crearSlice(data, idUser):
    print(data['vms'])
    try:
        result = ejecutarConsultaSQL("INSERT INTO slice (nombre, idOpenstackproject, idLinuxproject, usuario_idUsuario, fecha, sliceJSON) VALUES (%s, %s, %s, %s, %s, %s)",
                            (data['nombre'], "", "", idUser, data['fecha'], json.dumps(data)))
        return result
    except Exception as e:
        return e

def modificarSlice(data):
    pass