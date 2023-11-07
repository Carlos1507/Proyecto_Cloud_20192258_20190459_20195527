import questionary, requests
from colorama import Fore
import copy

class VM:
    def __init__(self, nombre, capacidad, cpu, imagen):
        self.nombre = nombre
        self.capacidad = capacidad
        self.cpu = cpu
        self.imagen = imagen
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'capacidad': self.capacidad,
            'cpu': self.cpu,
            'imagen': self.imagen
        }

def agregarVM(endpointBase):
    print(Fore.CYAN+"Creación de su máquina virtual:")
    nombreVM = questionary.text("Ingrese el nombre de la VM:").ask()
    capacidadVM = questionary.text("Ingrese la capacidad (Tamaño disco) en MB:").ask()
    cpuVM = questionary.text("Ingrese el número de cores para la VM (CPUs)").ask()
    response = requests.get(url = endpointBase+"/allImagenes", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        imagenes = response.json()['result']
        imagenesNombres = [imagen[1] for imagen in imagenes]
        imagenNombre = questionary.select("Seleccione una de las imágenes disponibles:", choices = imagenesNombres).ask()
        return VM(nombreVM, capacidadVM, cpuVM, imagenNombre).to_dict()   
    else:
        print(Fore.RED + "Error en el servidor, en este momento no se puede acceder a las imágenes")

def generarEnlace(listaVMs, listaEnlaces):
    listaNombresVMs = [vm['nombre'] for vm in listaVMs]
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
    listaNombresVMs = [vm['nombre'] for vm in listaVMs]
    vms_utilizadas  = set()
    for tupla in listaEnlaces:
        vms_utilizadas.update(tupla)
    vms_faltantes = []
    for vm in listaNombresVMs:
        if vm not in vms_utilizadas:
            vms_faltantes.append(vm)
    return vms_faltantes