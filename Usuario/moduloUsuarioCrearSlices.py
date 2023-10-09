import questionary
from colorama import Fore
import Usuario.moduloUsuarioGenerRecursos as recurso

def crearSlice(usuarioLog, endpointBase):
    title = "Seleccione un tipo de topología:"
    choicesCrear = ["1. Predeterminado", "2. Personalizado", "**Regresar**"]
    opcion = questionary.select(title, choices=choicesCrear).ask()    
    if (opcion == "**Regresar**"):
        return
    else:
        if(opcion == "1. Predeterminado"):
            topologiaPredeterminada(usuarioLog, endpointBase)
        elif(opcion == "2. Personalizado"):
            topologiaPersonalizada(usuarioLog, endpointBase)

def topologiaPredeterminada(usuarioLog, endpointBase):
    choicesPredeterminada = ["1. Malla","2. Árbol","3. Anillo","4. Lineal","5. Salir"]
    title = "Seleccione el tipo de topología:"
    opcion = questionary.select(title, choices=choicesPredeterminada).ask()

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