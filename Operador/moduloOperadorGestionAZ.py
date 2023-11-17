import questionary, requests, json
from colorama import Fore, Style, init

def zonasDisponibilidad(usuarioLog, endpointBase):
    print(Fore.CYAN+"Zonas de disponibilidad...")  
    opcion1 = "Plan 1: Silver Zone"
    opcion2 = "Plan 2: Gold Zone"
    choicesAZ = [opcion1, opcion2]
    opcion = questionary.select("Seleccione para visualizar las características del plan", choices=choicesAZ).ask()

    if(opcion == opcion1):
        pass
    else:
        pass