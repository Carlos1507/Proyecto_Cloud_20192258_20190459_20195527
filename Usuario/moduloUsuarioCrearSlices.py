import questionary, requests, time, json, datetime
from colorama import Fore
from rich.console import Console
from rich.table import Table
import Usuario.moduloUsuarioGenerRecursos as recurso
import Recursos.funcionEjecutarComandoRemoto as ejecutarComando
from Recursos.funcionGestionTopologias import graficarTopologia
from Recursos.funcionGestionTopologias import graficarTopologiaImportada
from Recursos.generarTopologiaArbol import generarArbol
from Recursos.generarTopologiaAnillo import generarAnillo
from Recursos.generarTopologiaMalla import generarMalla
from Recursos.generarTopologiaLineal import generarLineal
console = Console()

def crearSlice(usuarioLog, endpointBase):
    title = "Seleccione un tipo de topología:"
    choicesCrear = ["1. Predeterminado", "2. Personalizado", "3. Importar topología", "**Regresar**"]
    opcion = questionary.select(title, choices=choicesCrear).ask()    
    if (opcion == "**Regresar**"):
        return
    else:
        if(opcion == "1. Predeterminado"):
            topologiaPredeterminada(usuarioLog, endpointBase)
        elif(opcion == "2. Personalizado"):
            topologiaPersonalizada(usuarioLog, endpointBase)
        elif(opcion=="3. Importar topología"):
            importarTopologia(usuarioLog, endpointBase)

def importarTopologia(usuarioLog, endpointBase):
    filename = questionary.path("Seleccionar archivo para importar: ").ask()
    try:
        with open(filename, "r") as archivo:
            print(Fore.CYAN+"Cargando previsualización...")
            time.sleep(1)
            jsonfile = graficarTopologiaImportada(json.load(archivo))
            confirmationCrear = questionary.confirm("¿Desea crear este slice?").ask()
            if(confirmationCrear):
                validarSliceCrearRecursos(usuarioLog, endpointBase, jsonfile)
    except FileNotFoundError:
        print(Fore.RED+"El archivo no se encontró")
    except IOError:
        print(Fore.RED+"Ocurrió un error al intentar abrir el archivo")
    crearSlice(usuarioLog, endpointBase)

def topologiaPredeterminada(usuarioLog, endpointBase):
    choicesPredeterminada = ["1. Malla","2. Árbol","3. Anillo","4. Lineal","5. Salir"]
    title = "Seleccione el tipo de topología:"
    opcion = questionary.select(title, choices=choicesPredeterminada).ask()
    if(opcion =="5. Salir"):
        crearSlice(usuarioLog, endpointBase)
    else: 
        listaEnlaces, listaNodos = [], []
        if(opcion=="1. Malla"):
            numNodos = questionary.text("Ingrese el número de nodos").ask()
            titulo = "Malla con "+numNodos
            listaEnlaces, listaNodos = generarMalla(int(numNodos))
        elif(opcion=="2. Árbol"):
            niveles = questionary.text("Ingrese el número de niveles del árbol").ask()
            hijos = questionary.text("Ingrese el número de hijos por nodo").ask()
            titulo = "Arbol nivel "+niveles+" con "+hijos+" hijos por nodo"
            listaEnlaces, listaNodos = generarArbol(int(hijos), int(niveles))
        elif(opcion=="3. Anillo"):
            numNodos = questionary.text("Ingrese el número de nodos").ask()
            titulo = "Anillo con "+numNodos
            listaEnlaces, listaNodos = generarAnillo(int(numNodos))
        elif(opcion=="4. Lineal"):
            numNodos = questionary.text("Ingrese el número de nodos").ask()
            titulo = "Lineal con "+numNodos
            listaEnlaces, listaNodos = generarLineal(int(numNodos))
        confirmation = questionary.confirm("¿Desea tener una vista previa?").ask()

        if confirmation:
            graficarTopologia(titulo, listaNodos, listaEnlaces)

        comandoListarImages = "openstack image list --long -c Name | awk 'NR>2 {print $2}'"
        listaImagenes = ejecutarComando.execRemoto(comandoListarImages, "10.20.10.221").split("\n")
        imagen = questionary.select("Seleccione una imagen: ", choices=listaImagenes).ask()

        comandoListarFlavors = "openstack flavor list --long -c Name -c RAM -c Disk -c VCPUs --format json"
        listaFlavors = ejecutarComando.execRemoto(comandoListarFlavors, "10.20.10.221")
        flavors = json.loads(listaFlavors)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("N°",justify="center")
        table.add_column("Nombre", justify="center")
        table.add_column("RAM (MB)",justify="center")
        table.add_column("Disco (GB)", justify="left")
        table.add_column("N° Cores", justify="lef")
        index = 1
        for flavor in flavors:
            nombre = flavor['Name']
            ram = flavor['RAM']
            disk = flavor['Disk']
            cpus = flavor['VCPUs']
            table.add_row(str(index), nombre, str(ram), str(disk), str(cpus))
            index+=1
        console.print(table)
        flavorName = [flavor['Name'] for flavor in flavors]
        flavorChoosedName = questionary.select("Seleccione un flavor: ", choices=flavorName).ask()
        flavor_seleccionado = [flavor for flavor in flavors if flavor["Name"] == flavorChoosedName][0]
        print(flavor_seleccionado)
        VMsDetalladas = []
        for vm_name in listaNodos:
            VMsDetalladas.append(recurso.VM(vm_name, flavor_seleccionado['RAM'], flavor_seleccionado['VCPUs'], flavor_seleccionado['Disk'] , imagen).to_dict())
        fecha_actual = datetime.datetime.now()
        nombre = questionary.text("Ingrese un nombre para su slice").ask()
        slice = {"vms": VMsDetalladas, "enlaces":listaEnlaces, "nombre":nombre, "fecha":fecha_actual.strftime("%d/%m/%Y")}  
        confirmationCrear = questionary.confirm("¿Desea crear este slice?").ask()
        if(confirmationCrear):
            validarSliceCrearRecursos(usuarioLog, endpointBase, slice)
        else:
            crearSlice(usuarioLog, endpointBase)

def validarDisponibilidadServidor(usuarioLog, endpointBase):
    response = requests.get(url = endpointBase+"/disponible/"+str(usuarioLog.idUser), 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        respuestaServer = response.json()['result']
        if(respuestaServer == "Disponible"):
            print("Disponible")
            return True
        elif(respuestaServer == "Ocupado"):
            print("Ocupado")
            confirmReintentar = questionary.confirm("Servidor temporalmente ocupado, ¿reintentar nuevamente?...").ask()
            if(confirmReintentar):
                time.sleep(2)
                validarDisponibilidadServidor(usuarioLog, endpointBase)
            else:
                return False
    else:
        confirmReintentar = questionary.confirm("Problema con el servidor, reintentando").ask()
        if(confirmReintentar):
            time.sleep(1)
            validarDisponibilidadServidor(usuarioLog, endpointBase)
        else:
            return False

def crearRecursos(usuarioLog, endpointBase, data):
    print(data)
    response = requests.post(url = endpointBase+"/validacionRecursos/"+str(usuarioLog.idUser), 
                                headers = {"Content-Type": "application/json"}, data=json.dumps(data))
    if(response.status_code == 200):
        result = response.json()['result']
        if(result == "Slice creado exitosamente"):
            return True
        elif(result == "En este momentoNo se cuentan con los suficientes recursos para generar este slice"):
            return False
        else:
            return False
    else:
        print(Fore.RED+"Problema con el servidor")

def topologiaPersonalizada(usuarioLog, endpointBase):
    print(Fore.CYAN+"Usted está empezando con la creación de su topología...")
    print(Fore.CYAN+"Agregue al menos 2 VM y 1 enlace")
    print(Fore.CYAN+"Añada sus Máquinas virtuales...")
    listaVMs = []
    listaVMs.append(recurso.agregarVM(endpointBase))
    listaVMs.append(recurso.agregarVM(endpointBase))
    while(True):
        confirmVM = questionary.confirm("¿Desea añadir otra VM?").ask()
        if(confirmVM==True):
            listaVMs.append(recurso.agregarVM(endpointBase))
        else:
            break
    listaEnlaces = []
    listaEnlaces.append(recurso.generarEnlace(listaVMs, listaEnlaces))
    while(True):
        confirmLink = questionary.confirm("¿Desea añadir otro enlace?").ask()
        if(confirmLink==True):
            vm1, vm2 = recurso.generarEnlace(listaVMs, listaEnlaces)
            if ((vm1 is not None) and (vm2 is not None)):
                listaEnlaces.append((vm1, vm2))
            else:
                continue
        else:
            dispositivosLibres = recurso.dispositivosNoConectados(listaVMs, listaEnlaces)
            if (len(dispositivosLibres)==0):
                break
            else:
                print(Fore.RED+"No ha conectado todos sus dispositivos")
                vms_sin_conectar = dispositivosLibres
                for vm in vms_sin_conectar:
                    print(Fore.RED+"Nodo sin conectar: "+vm)
                continue
    confirmation = questionary.confirm("¿Desea tener una vista previa?").ask()
    listaVMsNombres = []
    for vm in listaVMs:
        listaVMsNombres.append(vm['nombre'])
    if confirmation:
        graficarTopologia("Diagrama Topología", listaVMsNombres,listaEnlaces)
    fecha_actual = datetime.datetime.now()
    nombre = questionary.text("Ingrese un nombre para su slice").ask()
    slice = {"vms": listaVMs, "enlaces":listaEnlaces, "nombre":nombre, "fecha":fecha_actual.strftime("%d/%m/%Y")}  
    confirmationCrear = questionary.confirm("¿Desea crear este slice?").ask()
    if(confirmationCrear):
        validarSliceCrearRecursos(usuarioLog, endpointBase, slice)
    else:
        crearSlice(usuarioLog, endpointBase)

def validarSliceCrearRecursos(usuarioLog, endpointBase, slice):
    if(validarDisponibilidadServidor(usuarioLog, endpointBase)):
        print(Fore.GREEN+"Servidor disponible, consultando recursos...")
        if(crearRecursos(usuarioLog, endpointBase, slice)):
            print(Fore.GREEN+"Slice creado exitosamente!")
            exportarConfirm = questionary.confirm("¿Exportar esta topología?").ask()
            if(exportarConfirm):
                nombreFile = questionary.text("Ingrese el nombre del archivo (sin extensión): ").ask()
                with open(nombreFile+".json", "w") as json_file:
                    json.dump(slice, json_file)
        else:
            print(Fore.RED+"No hay capacidad para alojar este slice")
    else:
        crearSlice(usuarioLog, endpointBase)