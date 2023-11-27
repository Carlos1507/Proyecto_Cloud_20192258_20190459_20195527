from rich.console import Console
from rich.table import Table
import requests, questionary
from colorama import Fore, Style, init
console = Console()
headers = {
            "Content-Type": "application/json",
            'X_APP_IDENTIFIER': "0a8cebdb56fdc2b22590690ebe5a3e2b",
           }

def gestionarSlices(usuario, endpointBase):

    response = requests.get(url = endpointBase+"/slice/listar", 
                                headers = headers)
    if(response.status_code == 200):
        slices = response.json()['result']
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("N°", justify="center")
        table.add_column("Usuario", justify="center")
        table.add_column("Nombre Slice",justify="center")
        table.add_column("Fecha", justify="center")
        table.add_column("Número VMs", justify="center")
        table.add_column("Número enlaces", justify="center")
        table.add_column("Zona de disponibilidad", justify="center")
        n = 1
        nombresSlices = []
        for slice in slices:
            username = slice['user']
            nombreSlice = slice['slice']['nombre']
            nombresSlices.append(nombreSlice)
            fecha = slice['slice']['fecha']
            numVMs = str(len(slice['slice']['sliceJSON']['vms']))
            numLinks = str(len(slice['slice']['sliceJSON']['enlaces']))
            az = slice['slice']['sliceJSON']['AZ']
            table.add_row(str(n),username, nombreSlice, fecha, numVMs, numLinks, az)
            n+=1
        console.print(table)
        confirmation = questionary.confirm("¿Desea eliminar algún slice?").ask()
        if(confirmation):
            nombreSelected = questionary.select("¿Cuál desea eliminar?", choices=nombresSlices).ask()
            for slice in slices:
                nombre = slice['slice']['nombre']
                if nombre == nombreSelected:
                    data = slice
                    break
            confirmation = questionary.confirm("¿Está seguro que desea eliminar este slice?\nEsta acción no es reversible").ask()
            if(confirmation):
                response = requests.delete(url = endpointBase+"/slice/eliminar/"+str(data['slice']['usuario_idUsuario'])+"/"+str(data['slice']['idSlice'])+"/"+str(data['slice']['nombre']), 
                                    headers = headers)
                if(response.status_code==200):
                    respuesta = response.json()['result']
                    if(respuesta == "Correcto"):
                        print(Fore.GREEN+"Slice eliminado")
                else:
                    print(Fore.RED+"Error"+response.status_code)
            else:
                return
    else:
        print(Fore.RED + "Error en el servidor")
    return