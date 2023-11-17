import questionary, requests
from colorama import Fore
import copy
from rich.console import Console
from rich.table import Table
console = Console()
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
                                        headers = {"Content-Type": "application/json"})
    imagenes = response.json()['result']
    imagenesOpciones = [imagen['nombre'] for imagen in imagenes]
    imagenChoosedName = questionary.select("Seleccione una imagen: ", choices=imagenesOpciones).ask()

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
    print(Fore.CYAN+"Conecte sus dispositivos")
    primeraVM = questionary.select("Seleccionar primer nodo", choices = listaNombresVMs).ask()
    choicesSegundaOpcion = copy.deepcopy(listaNombresVMs)
    choicesSegundaOpcion.remove(primeraVM)
    segundaVM = questionary.select("Seleccionar segundo nodo", choices = choicesSegundaOpcion).ask()
    if(((primeraVM, segundaVM) or (segundaVM, primeraVM) ) in listaEnlaces):
        print(Fore.CYAN+"Este enlace ya ha sido generado")
        if(len(listaEnlaces)==0):
            generarEnlace(listaVMs, listaEnlaces)
        else:
            return (None, None)
    else:
        return (primeraVM, segundaVM)
    
def dispositivosNoConectados(listaVMs, listaEnlaces):
    listaNombresVMs = [vm['alias'] for vm in listaVMs]
    vms_utilizadas  = set()
    for tupla in listaEnlaces:
        vms_utilizadas.update(tupla)
    vms_faltantes = []
    for vm in listaNombresVMs:
        if vm not in vms_utilizadas:
            vms_faltantes.append(vm)
    return vms_faltantes