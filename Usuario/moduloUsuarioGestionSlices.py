from rich.console import Console
from rich.table import Table
import requests, questionary, json
from colorama import Fore, Style, init
console = Console()

def gestionarSlicesUsuario(usuario, endpointBase):
    response = requests.get(url = endpointBase+"/slicesUser/"+str(usuario.idUser), 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        slices = response.json()['result']
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("N°",justify="center")
        table.add_column("Nombre",justify="center")
        table.add_column("Fecha", justify="left")
        table.add_column("Número Nodos", justify="lef")
        table.add_column("Número enlaces", justify="left")
        index = 1
        nombresSlices = []
        for slice in slices:
            idUser = next(iter(slice.keys()))
            nombre = slice[idUser]['nombre']
            nombresSlices.append(nombre)
            fecha = slice[idUser]['fecha']
            numVMs = str(len(slice[idUser]['vms']))
            numLinks = str(len(slice[idUser]['enlaces']))
            table.add_row(str(index), nombre, fecha, numVMs,numLinks)
            index+=1
        console.print(table)
        responseConfirm = questionary.confirm("¿Desea eliminar algún Slice?").ask()

        if(responseConfirm):
            nombreSlice = questionary.select("¿Cuál desea eliminar?", choices=nombresSlices).ask()
            
            for slice in slices:
                idUser = next(iter(slice.keys()))
                nombre = slice[idUser]['nombre']
                if nombre == nombreSlice:
                    data = slice
                    break
            response = requests.post(url = endpointBase+"/eliminarSlice/"+str(usuario.idUser), 
                                headers = {"Content-Type": "application/json"}, data=json.dumps(data))
            if(response.status_code==200):
                respuesta = response.json()['result']
                if(respuesta == "Eliminado con éxito"):
                    print(Fore.RED+"Slice eliminado")
    else:
        print(Fore.RED + "Error en el servidor")
    return