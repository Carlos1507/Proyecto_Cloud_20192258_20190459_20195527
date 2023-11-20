import random, os, paramiko, json
import json, os, platform
from modelosBD import *
sistema = platform.system()

if(sistema =="Linux"):
    from funcionConsultasBD import ejecutarSQLlocal as ejecutarConsultaSQL
else:
    from funcionConsultasBD import ejecutarSQLRemoto as ejecutarConsultaSQL


def validarRecursosDisponibles(data):
    resultW1 = ejecutarConsultaSQL("SELECT * FROM recursos where worker=%s", ("worker1",))[0]
    resultW2 = ejecutarConsultaSQL("SELECT * FROM recursos where worker=%s", ("worker2",))[0]
    worker1 = {"name":resultW1[1], 
               "ramDispo": int(resultW1[3])- int(resultW2[2]), 
               "discoDispo": int(resultW1[5])- int(resultW2[4]),
               "cpuDispo":int(resultW1[7])- int(resultW2[6])}
    worker2 = {"name":resultW2[1], 
               "ramDispo": int(resultW2[3])- int(resultW2[2]), 
               "discoDispo": int(resultW2[5])- int(resultW2[4]),
               "cpuDispo":int(resultW2[7])- int(resultW2[6])}
    listaVMs = data["vms"]

    for vm in listaVMs:
        validacionWorker1 = (vm['ram'] <= worker1["ramDispo"]) and (vm['cpu'] <= worker1['cpuDispo']) and (vm['disk'] <= worker1['discoDispo'])
        validacionWorker2 = (vm['ram'] <= worker2["ramDispo"]) and (vm['cpu'] <= worker2['cpuDispo']) and (vm['disk'] <= worker2['discoDispo'])
        if(validacionWorker1):
            # El worker1 tiene los recursos para alojar esta VM
            worker1['ramDispo'] -= vm['ram']
            worker1['cpuDispo'] -= vm['cpu']
            worker1["discoDispo"] -= vm['disk']
        elif(validacionWorker2):
            # El worker2 tiene los recursos para alojar esta VM
            worker2['ramDispo'] -= vm['ram']
            worker2['cpuDispo'] -= vm['cpu']
            worker2["discoDispo"] -= vm['disk']
        else:
            ### Esta VM no pasó ninguna validación y por tanto hay recursos suficientes para crear el slice
            print("El slice no se puede crear")
            return False    
    # Si llega aquí es porque todas las VMs han superado alguna validación y hay recursos suficientes para crearlas
    print("El slice se puede crear")
    return True

def consultarRecursosBD():
    result = ejecutarConsultaSQL("SELECT * FROM recursos", ())
    listaRecursos = []
    for elem in result:
        print(elem)
        listaRecursos.append(RecursosBD(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))
    return listaRecursos

def obtenerIDOpenstackProject(sliceName):
    if sistema == "Linux":
        proyectId = execLocal("openstack project show --format value --column id "+sliceName,"127.0.0.1")
    else:
        proyectId = execRemoto("openstack project show --format value --column id "+sliceName,"10.20.10.221")
    return proyectId

def execRemoto(command, host):
    username = "ubuntu"
    password = "ubuntu"
    client = paramiko.SSHClient()
    comandos = [". admin-openrc", command]
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, "5800", username,password
                       , key_filename="venv/headkey"
                       )
        
        _stdin, _stdout, _stderr = client.exec_command(comandos[0]+ " ; "+comandos[1])
        output = _stdout.read().decode().strip()
        error = _stderr.read().decode().strip()
        #print(f"Comando ejecutado: {command}")
        #print(f"Resultado: {output}")
        #print(f"Error: {error}")
        return output
    except Exception as e:
        print(f"Error {str(e)}")
    finally:
        client.close()

def execLocal(command, host):
    username = "ubuntu"
    password = "ubuntu"
    client = paramiko.SSHClient()
    comandos = [". admin-openrc", command]
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, "22", username,password)
        
        _stdin, _stdout, _stderr = client.exec_command(comandos[0]+ " ; "+comandos[1])
        output = _stdout.read().decode().strip()
        error = _stderr.read().decode().strip()
        #print(f"Comando ejecutado: {command}")
        #print(f"Resultado: {output}")
        #print(f"Error: {error}")
        return output
    except Exception as e:
        print(f"Error {str(e)}")
    finally:
        client.close()

def crearVM_BD(vm):
    if vm['alias'] != "":
        nombreVM = vm['alias']
    else:
        nombreVM = vm['nombre']
    try:
        ejecutarConsultaSQL("INSERT INTO vm (nombre, idopenstack, pid, flavors_idflavors, imagenes_idImagenes, slice_idSlice, linkAcceso) VALUES (%s, %s, %s, %s, %s, %s)",
                            (nombreVM, vm['idVM'], 0, vm['idOpenstackFlavor'], vm['idOpenstackImagen'], vm['idSliceBD'], vm['linkAcceso']))
        return "Exito"    
    except Exception as e:
        return e

def actualizarRecursosDisponibles():
    if(sistema=="Linux"):
         resultW1 = execLocal("openstack hypervisor show Worker1 -c vcpus_used -c local_gb_used -c memory_mb_used --format json","127.0.0.1")
         resultW2 = execLocal("openstack hypervisor show Worker2 -c vcpus_used -c local_gb_used -c memory_mb_used --format json","127.0.0.1")    
         resultW3 = execLocal("openstack hypervisor show Worker3 -c vcpus_used -c local_gb_used -c memory_mb_used --format json","127.0.0.1")
    else:
         resultW1 = execLocal("openstack hypervisor show Worker1 -c vcpus_used -c local_gb_used -c memory_mb_used --format json","10.20.10.221")
         resultW2 = execLocal("openstack hypervisor show Worker2 -c vcpus_used -c local_gb_used -c memory_mb_used --format json","10.20.10.221")
         resultW3 = execLocal("openstack hypervisor show Worker3 -c vcpus_used -c local_gb_used -c memory_mb_used --format json","10.20.10.221")

    recursosW1= json.loads(resultW1)
    recursosW2= json.loads(resultW2)
    recursosW3= json.loads(resultW3)
    
    ejecutarConsultaSQL("UPDATE recursos SET memoriaUso = %s, discoAsignado = %s, cpusAsignado = %s WHERE worker=%s",
                        (int(recursosW1['memory_mb_used']),int(recursosW1['local_gb_used'], int(recursosW1['vcpus_used']), "worker1")))
    ejecutarConsultaSQL("UPDATE recursos SET memoriaUso = %s, discoAsignado = %s, cpusAsignado = %s WHERE worker=%s",
                        (int(recursosW2['memory_mb_used']),int(recursosW2['local_gb_used'], int(recursosW2['vcpus_used']), "worker1")))
    ejecutarConsultaSQL("UPDATE recursos SET memoriaUso = %s, discoAsignado = %s, cpusAsignado = %s WHERE worker=%s",
                        (int(recursosW3['memory_mb_used']),int(recursosW3['local_gb_used'], int(recursosW3['vcpus_used']), "worker1")))

if __name__ == "__main__":
    resultado = execRemoto("openstack hypervisor list", "10.20.10.221")
    print(resultado)
