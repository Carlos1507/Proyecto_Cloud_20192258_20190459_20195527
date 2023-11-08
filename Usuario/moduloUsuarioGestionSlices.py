import questionary, requests, time, json, datetime
from rich.console import Console
from rich.table import Table
import requests, questionary, json
from colorama import Fore, Style, init
from Recursos.funcionGestionTopologias import graficarTopologiaImportada
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
        opcionesGestion = ["a. Editar Slices","b. Eliminar Slices","Regresar"]
        opcion = questionary.select("¿Desea editar o eliminar slices?", choices=opcionesGestion).ask()
        if(opcion == "Regresar"):
            return
        else:
            if(opcion=="b. Eliminar Slices"):
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
                nombreSlice = questionary.select("¿Cuál desea editar?", choices=nombresSlices).ask()
                for slice in slices:
                    idUser = next(iter(slice.keys()))
                    nombre = slice[idUser]['nombre']
                    if nombre == nombreSlice:
                        data = slice
                        break
                slice_data = list(data.values())[0] #Es un diccionario
                print(Fore.CYAN+"Cargando previsualización...")
                time.sleep(1)
                graficarTopologiaImportada(slice_data)
                opcionesEditar = ["1. Eliminar VM","2. Eliminar Enlace","Regresar"]
                opcion = questionary.select("¿Que acción realizará?", choices=opcionesEditar).ask()
                if(opcion == "Regresar"):
                    return
                else:
                    if(opcion=="1. Eliminar VM"):
                        slice_data_copia = slice_data
                        while True:
                            nombre_vm_a_eliminar = input("Ingrese el nombre de la VM a eliminar (o '0' para terminar): ")
                            if nombre_vm_a_eliminar.lower() == '0':
                                break
                            vms = slice_data_copia['vms']
                            enlaces = slice_data_copia['enlaces']

                            vm_existente = next((vm for vm in vms if vm['nombre'] == nombre_vm_a_eliminar), None)

                            if vm_existente is not None:
                                nueva_lista_vms = [vm for vm in vms if vm['nombre'] != nombre_vm_a_eliminar]
                                nuevos_enlaces = [enlace for enlace in enlaces if nombre_vm_a_eliminar not in enlace]
                                slice_data_copia['vms'] = nueva_lista_vms
                                slice_data_copia['enlaces'] = nuevos_enlaces
                                print(Fore.CYAN+"Cargando previsualización...")
                                time.sleep(1)
                                graficarTopologiaImportada(slice_data_copia)
                                if len(slice_data_copia['vms']) == 1:
                                    print(Fore.RED + "Solo queda una VM. No se pueden eliminar más.")
                                    break
                            else:
                                print(Fore.RED + "Nombre de VM no encontrado. Intente nuevamente.")

                        confirmEditar = questionary.confirm("¿Desea guardar los cambios?").ask()
                        if(confirmEditar):
                            print(Fore.CYAN+"Guardando cambios ...")
                            time.sleep(1)
                            # Poner el web service
                            print(Fore.GREEN+"Edición exitosa")
    else:
        print(Fore.RED + "Error en el servidor")
    return