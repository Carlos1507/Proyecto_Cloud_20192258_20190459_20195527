import questionary, requests
from colorama import Fore
import copy
from rich.console import Console
from rich.table import Table
console = Console()
headers = {
            "Content-Type": "application/json",
            'X_APP_IDENTIFIER': "0a8cebdb56fdc2b22590690ebe5a3e2b",
           }

class VM:
    def __init__(self, nombre, alias, ram, cpu, disk, imagen, idOpenstackImagen, idOpenstackFlavor):
        self.nombre = nombre
        self.alias = alias
        self.ram = ram
        self.cpu = cpu
        self.disk = disk
        self.imagen = imagen
        self.idOpenstackImagen = idOpenstackImagen
        self.idOpenstackFlavor = idOpenstackFlavor
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'alias': self.alias,
            'ram': self.ram,
            'cpu': self.cpu,
            'disk': self.disk,
            'imagen': self.imagen,
            'idOpenstackImagen': self.idOpenstackImagen,
            'idOpenstackFlavor': self.idOpenstackFlavor,
        }

def agregarVM(endpointBase, listaVMs):
    print(Fore.CYAN+"Creación de su máquina virtual:")

    while not (aliasVM := questionary.text("Ingrese el nombre de la VM:").ask().strip()):
                print(Fore.YELLOW + "El nombre no debe estar vacío")
    response = requests.get(url = endpointBase+"/imagenes/listar", 
                                        headers = headers)
    imagenes = response.json()['result']
    imagenesOpciones = [imagen['nombre'] for imagen in imagenes]
    print(Fore.CYAN+"================= IMÁGENES =================")
    imagenChoosedName = questionary.select("Seleccione una imagen: ", choices=imagenesOpciones).ask()

    response = requests.get(url = endpointBase+"/flavors/listar", 
                                    headers = headers)
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
    print(Fore.CYAN+"================= FLAVORS =================")
    flavorName = [flavor['nombre'] for flavor in flavors]
    flavorChoosedName = questionary.select("Seleccione un flavor: ", choices=flavorName).ask()
    flavor_seleccionado = [flavor for flavor in flavors if flavor["nombre"] == flavorChoosedName][0]
    imagen_seleccionado = [imagen for imagen in imagenes if imagen["nombre"] == imagenChoosedName][0]
    listaNombresVMs = [vm['nombre'] for vm in listaVMs]
    if(len(listaNombresVMs)==0):
        nombreVM = "vm1"
    else:
        ultimoValorVM = listaNombresVMs[-1]
        nombreVM = ultimoValorVM[:-1]+str(int(ultimoValorVM[-1])+1)
    return VM(nombreVM, aliasVM, flavor_seleccionado['ram'], flavor_seleccionado['cpu'], flavor_seleccionado['disk'] , imagen_seleccionado['filename'], imagen_seleccionado['idglance'], flavor_seleccionado['idflavorglance']).to_dict()   

def generarEnlace(listaVMs, listaEnlaces):
    listaNombresVMs = [vm['alias'] for vm in listaVMs]
    print(Fore.CYAN + "Conecte sus dispositivos")
    primeraVM_alias = questionary.select("Seleccionar primer nodo", choices=listaNombresVMs).ask()

    # Obtener el diccionario correspondiente al alias seleccionado
    primeraVM = next(vm for vm in listaVMs if vm['alias'] == primeraVM_alias)

    choicesSegundaOpcion = copy.deepcopy(listaNombresVMs)
    choicesSegundaOpcion.remove(primeraVM_alias)
    segundaVM_alias = questionary.select("Seleccionar segundo nodo", choices=choicesSegundaOpcion).ask()

    # Obtener el diccionario correspondiente al alias seleccionado
    segundaVM = next(vm for vm in listaVMs if vm['alias'] == segundaVM_alias)

    enlace = (primeraVM['nombre'], segundaVM['nombre'])

    if (enlace in listaEnlaces) or (enlace[::-1] in listaEnlaces):
        print(Fore.CYAN + "Este enlace ya ha sido generado")
        if len(listaEnlaces) == 0:
            generarEnlace(listaVMs, listaEnlaces)
        else:
            return (None, None)
    else:
        return enlace
    
def dispositivosNoConectados(listaVMs, listaEnlaces):
    listaNombresVMs = [vm['nombre'] for vm in listaVMs]
    vms_utilizadas  = set()
    for tupla in listaEnlaces:
        vms_utilizadas.update(tupla)
    vms_faltantes = []
    for vm in listaNombresVMs:
        if vm not in vms_utilizadas:
            vms_faltantes.append(vm)
    return vms_faltantes