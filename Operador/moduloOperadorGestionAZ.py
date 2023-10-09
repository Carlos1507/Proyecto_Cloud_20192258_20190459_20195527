import questionary, requests, json
from colorama import Fore, Style, init

def zonasDisponibilidad(usuarioLog, endpointBase):
    print(Fore.CYAN+"Definiendo zonas de disponibilidad...")  
    opcion1 = "Plan 1: Silver Zone"
    opcion2 = "Plan 2: Gold Zone"
    choicesAZ = [opcion1, opcion2]
    opcion = questionary.select("Seleccione el plan a configurar", choices=choicesAZ).ask()

    choicesRecursos = ["1 worker", "3 workers"]
    opcionRecursos = questionary.select("Seleccione recursos físicos", choices=choicesRecursos).ask()

    if(opcionRecursos=="1 worker"):
        AZs = ["Única Zona"]
    else:
        AZs = ["Zona Norte", "Zona Centro", "Zona Sur"]

    payload = {"azs": AZs}
    response = requests.post(url = endpointBase+"/guardarAZs", 
                                headers = {"Content-Type": "application/json"}, 
                                data= json.dumps(payload))
    if(response.status_code==200):
        print(Fore.GREEN+"Configuración exitosa")