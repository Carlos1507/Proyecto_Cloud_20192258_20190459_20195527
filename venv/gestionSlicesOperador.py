from rich.console import Console
from rich.table import Table
import requests
from colorama import Fore, Style, init
console = Console()

def gestionarSlices(usuario):

    response = requests.get(url = "http://127.0.0.1:8000/allSlices", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        slices = response.json()['result']
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("N°", justify="right")
        table.add_column("Nombre",justify="center")
        table.add_column("Fecha", justify="left")
        table.add_column("Número VMs", justify="lef")
        table.add_column("Número enlaces", justify="left")
        table.add_column("Activo", justify="left")
        for i in range(0, len(slices)):
            table.add_row(str(i+1), slices[i][0], slices[i][1], slices[i][2], slices[i][3], slices[i][4])
        console.print(table)
    else:
        print(Fore.RED + "Error en el servidor")
    return