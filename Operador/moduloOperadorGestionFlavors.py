import requests, questionary
from colorama import Fore
import json
from rich.console import Console
from Recursos.funcionEjecutarComandoRemoto import execRemoto
from rich.table import Table
console = Console()
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
    opcionesSubMenuFlavors = ["1. Definir nuevo flavor", "2. Listar flavors", "3. Eliminar flavor","4. Regresar"]
    opcion = questionary.select("Elija una opción: ", choices=opcionesSubMenuFlavors).ask()
    if(opcion =="4. Regresar"):
        return
    else:
        if(opcion == "1. Definir nuevo flavor"):
            crearFlavor(endpointBase)
        elif(opcion == "2. Listar flavors"):
            listarFlavors(endpointBase)
        elif(opcion == "3. Eliminar flavor"):
            eliminarFlavor(endpointBase)
def crearFlavor(endpointBase):
    ram_size = questionary.text("Indique el tamaño de la RAM en MB: ").ask()
    disk_size = questionary.text("Indique el tamaño del disco en GB: ").ask()
    num_cpus = questionary.text("Indique el número de cores (CPUs): ").ask()
    nombreFlavor = f"{ram_size}MBRAM_{num_cpus}VCPUs_{disk_size}GBRoot"
    comandoNewFlavor =f"openstack flavor create --ram {ram_size} --disk {disk_size} --vcpus {num_cpus} {nombreFlavor} --format json"
    outputjson = ejecutarComando.execRemoto(comandoNewFlavor, "10.20.10.221")
    jsonresponse = json.loads(outputjson)
    response = requests.post(url = endpointBase+ "/flavors/crear", 
                                headers = {"Content-Type": "application/json"}, data=json.dumps({"ram_mb":ram_size, "disk_gb":disk_size, "cpus":num_cpus, "nombre":nombreFlavor, "idflavorglance": jsonresponse['id']}))
    if(response.status_code==200 and response.json()['result']=="Correcto"):
        print(Fore.GREEN+"Imagen agregada exitosamente")
    else:
        print(Fore.RED+"Error en el servidor")

def listarFlavors(endpointBase):
    response = requests.get(url = endpointBase+"/flavors/listar", 
                                    headers = {"Content-Type": "application/json"})
    flavors = response.json()['result']
        
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("N°",justify="center")
    table.add_column("Nombre", justify="center")
    table.add_column("RAM (MB)",justify="center")
    table.add_column("Disco (GB)", justify="left")
    table.add_column("N° Cores", justify="lef")
    index = 1
    for flavor in flavors:
        nombre = flavor['nombre']
        ram = flavor['ram']
        disk = flavor['disk']
        cpus = flavor['cpu']
        table.add_row(str(index), nombre, str(ram), str(disk), str(cpus))
        index+=1
    console.print(table)

def eliminarFlavor(endpointBase):
    response = requests.get(url = endpointBase+"/flavors/listar", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        flavors = response.json()['result']
        flavorOpciones = [flavor['nombre'] for flavor in flavors]
        flavorNombre = questionary.rawselect("Elija una imagen a eliminar: ", choices=flavorOpciones).ask()
        flavor_seleccionado = [flavor for flavor in flavors if flavor["nombre"] == flavorNombre][0]
        resultadoEliminar = requests.get(url = endpointBase+"/flavors/eliminar/"+str(flavor_seleccionado['idflavors']), 
                                         headers = {"Content-Type": "application/json"})
        execRemoto("openstack flavor delete "+ flavor_seleccionado['idflavorglance'], "10.20.10.221")
        if(resultadoEliminar.status_code==200 and resultadoEliminar.json()["result"] == "Correcto"):
            print(Fore.GREEN+"Flavor Eliminado Correctamente")
        else:
            print(Fore.RED+"Hubo un problema al eliminar, intente nuevamente")
    else:
        print(Fore.RED + "Error en el servidor")
    gestorFlavors(endpointBase)