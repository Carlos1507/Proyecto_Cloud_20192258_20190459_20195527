from rich.console import Console
from rich.table import Table
import requests
from colorama import Fore, Style, init
console = Console()

def gestionarSlices(usuario, endpointBase):

    response = requests.get(url = endpointBase+"/allSlices", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        slices = response.json()['result']
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("idUser", justify="right")
        table.add_column("Nombre",justify="center")
        table.add_column("Fecha", justify="left")
        table.add_column("Número VMs", justify="left")
        table.add_column("Número enlaces", justify="left")
        
        for slice in slices:
            idUser = next(iter(slice.keys()))
            nombre = slice[idUser]['nombre']
            fecha = slice[idUser]['fecha']
            numVMs = str(len(slice[idUser]['vms']))
            numLinks = str(len(slice[idUser]['enlaces']))
            table.add_row(str(idUser), nombre, fecha, numVMs, numLinks)
        console.print(table)
    else:
        print(Fore.RED + "Error en el servidor")
    return