import questionary, requests, time, json, datetime
from colorama import Fore
import Usuario.moduloUsuarioGenerRecursos as recurso
from Recursos.funcionGestionTopologias import graficarTopologia
from Recursos.funcionGestionTopologias import importarTopolog

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
            importarTopolog(archivo)
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
        if(opcion=="1. Malla"):
            titulo = "Diagrama Topología: Malla"
            listaVMs = ["vm1", "vm2", "vm3", "vm4"]
            listaSWs = ["sw1", "sw2", "sw3", "sw4"]
            listaEnlaces = [("sw1","vm1"),("sw2","vm2"),("sw3","vm3"),("sw4","vm4"),
                            ("sw1","sw2"),("sw2", "sw3"),("sw3", "sw4"),("sw4","sw1"),
                            ("sw1","sw3"),("sw2","sw4")]
        elif(opcion=="2. Árbol"):
            titulo = "Diagrama Topología: Árbol"
            listaVMs = ["vm1", "vm2", "vm3", "vm4"]
            listaSWs = ["sw1", "sw2", "sw3", "sw4"]
            listaEnlaces = [("sw1","vm1"),("sw2","vm2"),("sw3","vm3"),("sw4","vm4"),
                            ("sw1","sw2"),("sw1","sw3"),("sw1","sw4")]
        elif(opcion=="3. Anillo"):
            titulo = "Diagrama Topología: Anillo"
            listaVMs = ["vm1", "vm2", "vm3", "vm4"]
            listaSWs = ["sw1", "sw2", "sw3", "sw4"]
            listaEnlaces = [("sw1","vm1"),("sw2","vm2"),("sw3","vm3"),("sw4","vm4"),
                            ("sw1","sw2"),("sw2", "sw3"),("sw3", "sw4"),("sw4","sw1")]
        elif(opcion=="4. Lineal"):
            titulo = "Diagrama Topología: Lineal"
            listaVMs = ["vm1", "vm2", "vm3"]
            listaSWs = ["sw1", "sw2", "sw3"]
            listaEnlaces = [("sw1","vm1"),("sw2","vm2"),("sw3","vm3"),
                            ("sw1","sw2"),("sw2", "sw3")]  
        confirmation = questionary.confirm("¿Desea tener una vista previa?").ask()

        if confirmation:
            graficarTopologia(titulo, listaVMs, listaSWs,listaEnlaces)
        if opcion == "4. Lineal":
            VMsDetalladas = [recurso.VM("vm1","1024","2","cirros.img").to_dict(), 
                             recurso.VM("vm2","1024","2","cirros.img").to_dict(),
                             recurso.VM("vm3","1024","2","cirros.img").to_dict()]
        else:
            VMsDetalladas = [recurso.VM("vm1","1024","2","cirros.img").to_dict(), 
                             recurso.VM("vm2","1024","2","cirros.img").to_dict(),
                             recurso.VM("vm3","1024","2","cirros.img").to_dict(),
                             recurso.VM("vm4","1024","2","cirros.img").to_dict()]
        fecha_actual = datetime.datetime.now()
        nombre = questionary.text("Ingrese un nombre para su slice").ask()
        slice = {"vms": VMsDetalladas, "switches": listaSWs, "enlaces":listaEnlaces, "nombre":nombre, "fecha":fecha_actual.strftime("%d/%m/%Y")}  
        confirmationCrear = questionary.confirm("¿Desea crear este slice?").ask()
        if(confirmationCrear):
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
    print(Fore.CYAN+"Agregue al menos 1 VM, 1 Switch y 1 enlace")
    print(Fore.CYAN+"Añada sus Máquinas virtuales...")
    listaVMs = []
    listaVMs.append(recurso.agregarVM(endpointBase))
    while(True):
        confirmVM = questionary.confirm("¿Desea añadir otra VM?").ask()
        if(confirmVM==True):
            listaVMs.append(recurso.agregarVM(endpointBase))
        else:
            break
    listaSwitches = []
    listaSwitches.append(recurso.agregarSwitch())
    while(True):
        confirmSW = questionary.confirm("¿Desea añadir otro switch?").ask()
        if(confirmSW==True):
            listaSwitches.append(recurso.agregarSwitch())
        else:
            break
    listaEnlaces = []
    listaEnlaces.append(recurso.generarEnlace(listaVMs, listaSwitches, listaEnlaces))
    while(True):
        confirmLink = questionary.confirm("¿Desea añadir otro enlace?").ask()
        if(confirmLink==True):
            listaEnlaces.append(recurso.generarEnlace(listaVMs, listaSwitches, listaEnlaces))
        else:
            dispositivosLibres = recurso.dispositivosNoConectados(listaVMs, listaSwitches, listaEnlaces)
            if((len(dispositivosLibres[0])==0) and (len(dispositivosLibres[1])==0)):
                break
            else:
                print(Fore.RED+"No ha conectado todos sus dispositivos")
                vms_sin_conectar = dispositivosLibres[0]
                for vm in vms_sin_conectar:
                    print(Fore.RED+"VM sin conectar: "+vm)
                switches_sin_conectar = dispositivosLibres[1]
                for switch in switches_sin_conectar:
                    print(Fore.RED+"Switch sin conectar: "+switch)
                continue
    confirmation = questionary.confirm("¿Desea tener una vista previa?").ask()
    listaSWsNombres = []
    for vm in listaVMs:
        listaSWsNombres.append(vm['nombre'])
    if confirmation:
        graficarTopologia("Diagrama Topología", listaSWsNombres, listaSwitches,listaEnlaces)
    fecha_actual = datetime.datetime.now()
    nombre = questionary.text("Ingrese un nombre para su slice").ask()
    slice = {"vms": listaVMs, "switches": listaSwitches, "enlaces":listaEnlaces, "nombre":nombre, "fecha":fecha_actual.strftime("%d/%m/%Y")}  
    confirmationCrear = questionary.confirm("¿Desea crear este slice?").ask()
    if(confirmationCrear):
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
    else:
        crearSlice(usuarioLog, endpointBase)