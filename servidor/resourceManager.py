import random, os, paramiko, json

def validarRecursosDisponibles(data):
    suma_ram = 0
    suma_cpu = 0
    suma_disk = 0
    for vm in data["vms"]:
        suma_ram += vm["ram"]
        suma_cpu += vm["cpu"]
        suma_disk += vm["disk"]
    print("Suma de RAM:", suma_ram)
    print("Suma de CPUs:", suma_cpu)
    print("Suma de Disk:", suma_disk)
    resultW1 = execRemoto("openstack hypervisor show Worker1 -c vcpus -c vcpus_used -c local_gb -c local_gb_used -c memory_mb -c memory_mb_used --format json","10.20.10.221")
    resultW2 = execRemoto("openstack hypervisor show Worker2 -c vcpus -c vcpus_used -c local_gb -c local_gb_used -c memory_mb -c memory_mb_used --format json","10.20.10.221")
    resultW3 = execRemoto("openstack hypervisor show Worker3 -c vcpus -c vcpus_used -c local_gb -c local_gb_used -c memory_mb -c memory_mb_used --format json","10.20.10.221")
    recursosW1= json.loads(resultW1)
    recursosW2= json.loads(resultW2)
    recursosW3= json.loads(resultW3)
    print("Se requiere: ")
    print("RAM:", suma_ram, "CPUs:", suma_cpu, "Disk:", suma_disk)
    print("En el Worker1 se tiene disponible:")
    print("RAM:", int(recursosW1['memory_mb'])-int(recursosW1['memory_mb_used']) , "CPUs:", int(recursosW1['vcpus'])-int(recursosW1['vcpus_used']), "Disk:",  int(recursosW1['local_gb'])-int(recursosW1['local_gb_used']))
    print("En el Worker2 se tiene disponible:")
    print("RAM:", int(recursosW2['memory_mb'])-int(recursosW2['memory_mb_used']) , "CPUs:", int(recursosW2['vcpus'])-int(recursosW2['vcpus_used']), "Disk:",  int(recursosW2['local_gb'])-int(recursosW2['local_gb_used']))
    print("En el Worker3 se tiene disponible:")
    print("RAM:", int(recursosW3['memory_mb'])-int(recursosW3['memory_mb_used']) , "CPUs:", int(recursosW3['vcpus'])-int(recursosW3['vcpus_used']), "Disk:",  int(recursosW3['local_gb'])-int(recursosW3['local_gb_used']))

    choices = [True, True, True, True, True, False]
    return random.choice(choices)


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