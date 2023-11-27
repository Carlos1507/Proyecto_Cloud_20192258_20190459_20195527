import questionary, requests, json
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init

console = Console()
headers = {
            "Content-Type": "application/json",
            'X_APP_IDENTIFIER': "0a8cebdb56fdc2b22590690ebe5a3e2b",
           }

def zonasDisponibilidad(usuarioLog, endpointBase):
    print(Fore.CYAN+"Zonas de disponibilidad...")  
    opcion1 = "Plan 1: Silver Zone"
    opcion2 = "Plan 2: Golden Zone"
    choicesAZ = [opcion1, opcion2]
    opcion = questionary.select("Seleccione para visualizar las características del plan", choices=choicesAZ).ask()
    
    response = requests.get(url = endpointBase+"/recursos/listar", headers = headers)
    recursos = response.json()['result']
    
    if(opcion == opcion1):  # SILVER
        workerNames = ["worker3"]
        data = []
        for recurso in recursos:
            if(recurso['worker'] in workerNames):
                data.append(recurso)
        generTabla(data)
    else: # GOLDEN
        workerNames = ["worker1", "worker2"]
        data = []
        for recurso in recursos:
            if(recurso['worker'] in workerNames):
                data.append(recurso)
        generTabla(data)
def generTabla(workers):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("N°", justify="center")
    table.add_column("Worker", justify="center")
    table.add_column("RAM en Uso (MB)",justify="center")
    table.add_column("RAM Total (MB)", justify="center")
    table.add_column("Disco Asignado (GB)", justify="center")
    table.add_column("Disco Total (GB)", justify="center")
    table.add_column("CPU Asignado", justify="center")
    table.add_column("CPU Total", justify="center")
    n = 1
    for worker in workers:
        workerName = worker['worker']
        RAMUso = str(worker['memoriaUso'])
        RAMTotal = str(worker['memoriaTotal'])
        DiscoAsig = str(worker['discoAsignado'])
        DiscoTotal = str(worker['discoTotal'])
        CPUAsig = str(worker['cpusAsignado'])
        CPUTotal = str(worker['cpuTotal'])
        table.add_row(str(n),workerName, RAMUso, RAMTotal, DiscoAsig, DiscoTotal, CPUAsig, CPUTotal)
        n+=1
    console.print(table)