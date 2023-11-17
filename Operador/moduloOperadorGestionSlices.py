from rich.console import Console
from rich.table import Table
import requests
from colorama import Fore, Style, init
console = Console()

def gestionarSlices(usuario, endpointBase):

    response = requests.get(url = endpointBase+"/slice/listar", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        slices = response.json()['result']
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("N°", justify="center")
        table.add_column("Usuario", justify="center")
        table.add_column("Nombre Slice",justify="center")
        table.add_column("Fecha", justify="center")
        table.add_column("Número VMs", justify="center")
        table.add_column("Número enlaces", justify="center")
        n = 1
        for slice in slices:
            username = slice['user']
            nombreSlice = slice['slice']['nombre']
            fecha = slice['slice']['fecha']
            numVMs = str(len(slice['slice']['sliceJSON']['vms']))
            numLinks = str(len(slice['slice']['sliceJSON']['enlaces']))
            table.add_row(str(n),username, nombreSlice, fecha, numVMs, numLinks)
            n+=1
        console.print(table)
    else:
        print(Fore.RED + "Error en el servidor")
    return