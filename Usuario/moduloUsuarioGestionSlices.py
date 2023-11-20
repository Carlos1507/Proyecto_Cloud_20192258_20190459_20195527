import questionary, requests, time, json, datetime
from rich.console import Console
import copy
from rich.table import Table
import requests, questionary, json
from colorama import Fore, Style, init
from Recursos.funcionGestionTopologias import graficarTopologiaImportada
import networkx as nx
from datetime import datetime

G = nx.Graph()
console = Console()

def gestionarSlicesUsuario(usuario, endpointBase):
    response = requests.get(url = endpointBase+"/slice/listarPorUsuario/"+str(usuario.idUser), 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        slices = response.json()['result']

        if(len(slices) == 0):
            print(Fore.YELLOW+"Usted aún no tiene slices creados")
        else:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("N°",justify="center")
            table.add_column("Nombre Slice",justify="center")
            table.add_column("Fecha", justify="center")
            table.add_column("Número Nodos", justify="center")
            table.add_column("Número enlaces", justify="center")
            table.add_column("Zona de disponibilidad", justify="center")
            index = 1
            nombresSlices = []
            for slice in slices:
                nombreSlice = slice['nombre']
                nombresSlices.append(nombreSlice)
                fecha = slice['fecha']
                numVMs = str(len(slice['sliceJSON']['vms']))
                numLinks = str(len(slice['sliceJSON']['enlaces']))
                az = slice['sliceJSON']['AZ']
                table.add_row(str(index), nombreSlice, fecha, numVMs,numLinks, az)
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
                        nombre = slice['nombre']
                        if nombre == nombreSlice:
                            data = slice
                            break
                    confirmation = questionary.confirm("¿Está seguro que desea eliminar este slice?\nEsta acción no es reversible").ask()
                    if(confirmation):
                        response = requests.delete(url = endpointBase+"/slice/eliminar/"+str(usuario.idUser)+"/"+str(data['idSlice'])+"/"+str(data['nombre']), 
                                            headers = {"Content-Type": "application/json"})
                        if(response.status_code==200):
                            respuesta = response.json()['result']
                            if(respuesta == "Eliminado con éxito"):
                                print(Fore.RED+"Slice eliminado")
                    else:
                        return
                else:
                    nombreSlice = questionary.select("¿Cuál desea editar?", choices=nombresSlices).ask()
                    for slice in slices:
                        nombre = slice['nombre']
                        if nombre == nombreSlice:
                            data = slice
                            break
                    slice_data = data['sliceJSON'] #Es un diccionario
                    slice_data_copia = copy.deepcopy(slice_data)
                    opcionesEditar = ["1. Eliminar VM","2. Eliminar Enlace","3. Agregar Enlace","4. Agregar VM","Regresar"]
                    opcion = questionary.select("¿Que acción realizará?", choices=opcionesEditar).ask()
                    if(opcion == "Regresar"):
                        return
                    else:
                        if(opcion=="1. Eliminar VM"):
                            print(Fore.CYAN+"Cargando previsualización...")
                            time.sleep(1)
                            graficarTopologiaImportada(slice_data)
                            eliminarVM(slice_data_copia)
                        elif(opcion=="2. Eliminar Enlace"):
                            print(Fore.CYAN+"Cargando previsualización...")
                            time.sleep(1)
                            graficarTopologiaImportada(slice_data)
                            eliminarEnlace(slice_data_copia)
                        elif(opcion=="3. Agregar Enlace"):
                            print(Fore.CYAN+"Cargando previsualización...")
                            time.sleep(1)
                            graficarTopologiaImportada(slice_data)
                            agregarEnlace(slice_data_copia)
                        elif(opcion=="4. Agregar VM"):
                            agregarVM(slice_data_copia, endpointBase)
                        else:
                            return
    else:
        print(Fore.RED + "Error en el servidor")
    return


def eliminarVM(slice_data_copia):
    alMenosUnaVez = 0
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
            alMenosUnaVez = 1
            print(Fore.CYAN+"Cargando previsualización...")
            time.sleep(1)
            graficarTopologiaImportada(slice_data_copia)
            if len(slice_data_copia['vms']) == 1:
                print(Fore.RED + "Solo queda una VM. No se pueden eliminar más.")
                break
        else:
            print(Fore.RED + "Nombre de VM no encontrado. Intente nuevamente.")

    if (alMenosUnaVez != 0):
        confirmEditar = questionary.confirm("¿Desea guardar los cambios?").ask()
        if(confirmEditar):
            print(Fore.CYAN+"Guardando cambios ...")
            time.sleep(1)
            slice_data_copia["fecha"] = datetime.now().strftime("%d/%m/%Y")
            # Poner el web service
            print(Fore.GREEN+"Edición exitosa")

def eliminarEnlace(slice_data_copia):
    alMenosUnaVez = 0
    limite_eliminacion = len(slice_data_copia['enlaces'])
    while True:
        # Salir del bucle si se alcanza el límite de eliminación
        if limite_eliminacion == 0:
            print(Fore.RED + "Se han eliminado todos los enlaces. No se pueden eliminar más.")
            break

        # Crear el grafo y los enlaces en cada iteración
        G.clear()
        nombresVMs = [vm['nombre'] for vm in slice_data_copia['vms']]
        links = slice_data_copia['enlaces']

        G.add_nodes_from(nombresVMs)
        G.add_edges_from(links)

        # Mostrar información actual
        edge_labels = {arista: f"Enlace {i + 1}" for i, arista in enumerate(G.edges())}

        nombre_enlace_a_eliminar = input("Ingrese el nombre del enlace a eliminar (o '0' para terminar): ")

        # Salir del bucle si el usuario lo desea
        if nombre_enlace_a_eliminar.lower() == '0':
            break

        # Buscar la arista correspondiente al nombre del enlace ingresado
        arista_a_eliminar = None
        for arista, label in edge_labels.items():
            if label == nombre_enlace_a_eliminar:
                arista_a_eliminar = arista
                break

        # Si se encontró la arista a eliminar, eliminarla del grafo y actualizar datos
        if arista_a_eliminar:
            G.remove_edge(*arista_a_eliminar)
            slice_data_copia['enlaces'] = [list(arista) for arista in G.edges()]
            limite_eliminacion -= 1  # Reducir el límite después de cada eliminación
            print(Fore.CYAN+"Cargando previsualización...")
            time.sleep(1)
            graficarTopologiaImportada(slice_data_copia)
            alMenosUnaVez = 1
        else:
            print(Fore.RED + "Nombre de enlace no encontrado. Intente nuevamente.")

    if (alMenosUnaVez != 0):
        confirmEditar = questionary.confirm("¿Desea guardar los cambios?").ask()
        if(confirmEditar):
            print(Fore.CYAN+"Guardando cambios ...")
            time.sleep(1)
            slice_data_copia["fecha"] = datetime.now().strftime("%d/%m/%Y")
            # Poner el web service
            print(Fore.GREEN+"Edición exitosa")

def agregarEnlace(datos):
    alMenosUnaVez = 0

    while True:
        vm1 = input("Ingrese el nombre de la primera VM (o escriba '0' para terminar): ")
        if vm1.lower() == '0':
            break
        
        if not vm1 in [info_vm["nombre"] for info_vm in datos["vms"]]:
            print(Fore.RED + f"No se encontró '{vm1}' en el slice. Ingrese un nombre válido.")
            continue

        vm2 = input("Ingrese el nombre de la segunda VM: ")

        # Validar si la segunda VM existe
        if not vm2 in [info_vm["nombre"] for info_vm in datos["vms"]]:
            print(Fore.RED + f"No se encontró '{vm2}' en el slice. Ingrese un nombre válido.")
            continue

        if vm1 == vm2:
            print(Fore.RED + "Los nombres de la VM's no pueden ser el mismo")
            continue

        enlace = [vm1, vm2]

        # Validar si ya existe un enlace entre las dos VM
        if enlace in datos["enlaces"] or enlace[::-1] in datos["enlaces"]:
            print(Fore.RED + f"Ya existe un enlace entre '{vm1}' y '{vm2}'. Por favor, ingrese VM's diferentes.")
            continue

        # Crear el enlace
        datos["enlaces"].append(enlace)
        alMenosUnaVez = 1

        print(Fore.CYAN+"Cargando previsualización...")
        time.sleep(1)
        graficarTopologiaImportada(datos)

    if (alMenosUnaVez != 0):
        confirmEditar = questionary.confirm("¿Desea guardar los cambios?").ask()
        if(confirmEditar):
            print(Fore.CYAN+"Guardando cambios ...")
            time.sleep(1)
            datos["fecha"] = datetime.now().strftime("%d/%m/%Y")
            # Poner el web service
            print(Fore.GREEN+"Edición exitosa")

def agregarVM(datos, endpointBase):
    responseFlavor = requests.get(url = endpointBase+"/flavors/listar", 
                                headers = {"Content-Type": "application/json"})
    flavours = responseFlavor.json()['result']
    
    responseImagenes = requests.get(url = endpointBase+"/imagenes/listar", 
                                headers = {"Content-Type": "application/json"})
    imagenes = responseImagenes.json()['result']
    alMenosUnaVez = 0

    while True:
        # Encontrar el último nombre de las máquinas virtuales
        ultima_vm = max((vm["nombre"] for vm in datos["vms"]), default="vm0")

        # Generar el nombre para la nueva VM
        numero_nueva_vm = int(ultima_vm[2:]) + 1
        nombre_nueva_vm = f"vm{numero_nueva_vm}"

        # Mostrar opciones de flavours
        print(Fore.CYAN+"Opciones de Flavors:")
        for i, flavour in enumerate(flavours, start=1):
            print(f"{i}. {flavour['nombre']} - RAM: {flavour['ram']}, CPU: {flavour['cpu']}, Disco: {flavour['disk']}")

        # Solicitar al usuario que elija un flavour
        print(Fore.CYAN+"================= FLAVORS =================")
        while True:
            try:
                opcion_flavour = int(input("Seleccione el número del flavour para la nueva VM: "))
                if 1 <= opcion_flavour <= len(flavours):
                    seleccion_flavour = flavours[opcion_flavour - 1]
                    break
                else:
                    print(Fore.RED+"Selección inválida. Intente nuevamente.")
            except ValueError:
                print(Fore.RED+"Ingrese un número entero válido.")

        # Mostrar opciones de imágenes
        print(Fore.CYAN+"Opciones de Imágenes:")
        for i, imagen in enumerate(imagenes, start=1):
            print(f"{i}. {imagen['nombre']}")

        # Solicitar al usuario que elija una imagen
        print(Fore.CYAN+"================= IMÁGENES =================")
        while True:
            try:
                opcion_imagen = int(input("Seleccione el número de la imagen para la nueva VM: "))
                if 1 <= opcion_imagen <= len(imagenes):
                    seleccion_imagen = imagenes[opcion_imagen - 1]
                    break
                else:
                    print(Fore.RED+"Selección inválida. Intente nuevamente.")
            except ValueError:
                print(Fore.RED+"Ingrese un número entero válido.")

        # Crear la nueva VM y agregarla a "vms"
        nueva_vm = {
                            "nombre": nombre_nueva_vm,
                            "alias": "",
                            "ram": seleccion_flavour['ram'],
                            "cpu": seleccion_flavour['cpu'],
                            "disk": seleccion_flavour['disk'],
                            "imagen": seleccion_imagen['filename'],
                            "idOpenstackImagen": seleccion_imagen['idglance'],
                            "idOpenstackFlavor": seleccion_flavour['idflavorglance']
                    }
        datos["vms"].append(nueva_vm)
        print(Fore.GREEN+f"Máquina virtual '{nombre_nueva_vm}' creada con éxito.")

        # Preguntar si desea crear enlace con otra VM
        confirmAgregar = questionary.confirm("¿Desea crear enlace con otra VM?").ask()
        if(confirmAgregar):
            print(Fore.CYAN+"Cargando previsualización...")
            time.sleep(1)
            graficarTopologiaImportada(datos)
            vm1 = input("Ingrese el nombre de VM con la cual enlazará la nueva VM: ")
            if not vm1 in [info_vm["nombre"] for info_vm in datos["vms"]]:
                print(Fore.RED + f"No se encontró '{vm1}' en el slice. Ingrese un nombre válido.")
                continue
            if vm1 == nombre_nueva_vm:
                print(Fore.RED + "Los nombres de la VM's no pueden ser el mismo")
                continue
            enlace = [vm1, nombre_nueva_vm]
            datos["enlaces"].append(enlace)
            print(Fore.CYAN+"Cargando previsualización...")
            time.sleep(1)
            graficarTopologiaImportada(datos)

        alMenosUnaVez = 1
        # Preguntar si el usuario desea agregar otra VM
        confirmAgregar = questionary.confirm("¿Desea agregar otra máquina virtual?").ask()
        if(not confirmAgregar):
            break

    if (alMenosUnaVez != 0):
        confirmEditar = questionary.confirm("¿Desea guardar los cambios?").ask()
        if(confirmEditar):
            print(Fore.CYAN+"Guardando cambios ...")
            time.sleep(1)
            datos["fecha"] = datetime.now().strftime("%d/%m/%Y")
            # Poner el web service
            print(Fore.GREEN+"Edición exitosa")