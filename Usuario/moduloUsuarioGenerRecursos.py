import questionary, requests
from colorama import Fore

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
    cpuVM = questionary.text("Ingres el número de cores para la VM (CPUs)").ask()
    response = requests.get(url = endpointBase+"/allImagenes", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        imagenes = response.json()['result']
        imagenesNombres = [imagen[1] for imagen in imagenes]
        imagenNombre = questionary.select("Seleccione una de las imágenes disponibles:", choices = imagenesNombres).ask()
        return VM(nombreVM, capacidadVM, cpuVM, imagenNombre).to_dict()   
    else:
        print(Fore.RED + "Error en el servidor, en este momento no se puede acceder a las imágenes")

def agregarSwitch():
    print(Fore.CYAN+"Creación de su switch:")
    nombreSW = questionary.text("Ingrese el nombre del switch:").ask()
    return nombreSW

def generarEnlace(listaVMs, listaSwitches, listaEnlaces):
    listaNombresVMs = [vm['nombre'] for vm in listaVMs]
    if(len(listaSwitches)>=2):
        choicesTiposEnlace = ["Conectar Switch - Switch", "Conectar Switch - Máquina virtual"]
    else:
        choicesTiposEnlace = ["Conectar Switch - Máquina virtual"]
    opcion = questionary.select("Elija un tipo de conexión", choices = choicesTiposEnlace).ask()
    if(opcion == "Conectar Switch - Switch"):
        primerSwitch = questionary.select("Seleccionar primer switch", choices = listaSwitches).ask()
        choicesSegundaOpcion = listaSwitches
        choicesSegundaOpcion.remove(primerSwitch)
        segundoSwitch = questionary.select("Seleccionar primer switch", choices = choicesSegundaOpcion).ask()
        return (primerSwitch, segundoSwitch)
    elif(opcion == "Conectar Switch - Máquina virtual"):
        switch = questionary.select("Seleccionar switch", choices = listaSwitches).ask()
        vm = questionary.select("Seleccionar VM", choices = listaNombresVMs).ask()
        return (switch, vm)

def dispositivosNoConectados(listaVMs, listaSwitches, listaEnlaces):
    listaNombresVMs = [vm['nombre'] for vm in listaVMs]
    conjunto_tuplas = set()
    conjunto_vms = set(listaNombresVMs)
    conjunto_switches = set(listaSwitches)
    for tupla in listaEnlaces:
        conjunto_tuplas.update(tupla)
    vms_sin_enlace = conjunto_vms - conjunto_tuplas
    switches_sin_enlace = conjunto_switches - conjunto_tuplas
    return (list(vms_sin_enlace), list(switches_sin_enlace))