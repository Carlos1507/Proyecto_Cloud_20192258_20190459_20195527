from rich.console import Console
from rich.table import Table
import requests
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
        for slice in slices:
            table.add_row(slice[0], slice[1], slice[2], slice[3], slice[4], slice[5])
        console.print(table)
    else:
        print(Fore.RED + "Error en el servidor")
    return