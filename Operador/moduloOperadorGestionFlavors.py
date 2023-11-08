import requests, questionary
from colorama import Fore
import json
import Recursos.funcionEjecutarComandoRemoto as ejecutarComando
def gestorImagenesGlance(endpointBase, nombre, filename):
    comando = f"glance image-create --name {nombre} --file /home/ubuntu/imagenes/{filename} "+ \
               "--disk-format qcow2 --container-format bare --visibility=public"
    ejecutarComando.execRemoto(comando, "10.20.10.221")
    comprobarImagen = f"openstack image list --name {nombre} -c Status -f value"
    output = ejecutarComando.execRemoto(comprobarImagen, "10.20.10.221")
    if (output=="active"):
        return True
    else:
        return False
def gestorFlavors(endpointBase):
    print(Fore.CYAN+"Gestionando flavors del sistema...")
    print(Fore.CYAN+"Estas serán las opciones que tendrán disponibles los usuarios al deplegar VMs")
    opcionesSubMenuFlavors = ["1. Definir nuevo flavor", "2. Listar flavors"]
    opcion = questionary.select("Elija una opción: ", choices=opcionesSubMenuFlavors).ask()
    if(opcion =="4. Regresar"):
        return
    else:
        if(opcion == "1. Definir nuevo flavor"):
            crearFlavor(endpointBase)
        elif(opcion == "2. Listar flavors"):
            listarFlavors(endpointBase)
def crearFlavor(endpointBase):
    ram_size = questionary.text("Indique el tamaño de la RAM en MB: ").ask()
    disk_size = questionary.text("Indique el tamaño del disco en GB: ").ask()
    num_cpus = questionary.text("Indique el número de cores (CPUs): ").ask()
    nombreFlavor = f"{ram_size}MBRAM_{num_cpus}VCPUs_{disk_size}GBRoot"
    comandoNewFlavor =f"openstack flavor create --ram {ram_size} --disk {disk_size} --vcpus {num_cpus} {nombreFlavor} --format json"
    outputjson = ejecutarComando.execRemoto(comandoNewFlavor, "10.20.10.221")
    jsonresponse = json.loads(outputjson)
    response = requests.post(url = endpointBase+ "/saveFlavor", 
                                headers = {"Content-Type": "application/json"}, data=json.dumps({"ram_mb":ram_size, "disk_gb":disk_size, "cpus":num_cpus, "nombre":nombreFlavor, "idflavorglance": jsonresponse['id']}))
    if(response.status_code==200 and response.json()['result']=="Correcto"):
        print(Fore.GREEN+"Imagen agregada exitosamente")
    else:
        print(Fore.RED+"Error en el servidor")

def listarFlavors(endpointBase):
    comandoListFlavors =f"openstack flavor list"
    ejecutarComando.execRemoto(comandoListFlavors, "10.20.10.221")