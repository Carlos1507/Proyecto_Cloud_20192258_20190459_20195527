import questionary, requests, time, json, datetime, os
from colorama import Fore
from rich.console import Console
from rich.table import Table
import Usuario.moduloUsuarioGenerRecursos as recurso
import Recursos.funcionEjecutarComandoRemoto as ejecutarComando
from Recursos.funcionGestionTopologias import graficarTopologia
from Recursos.funcionGestionTopologias import graficarTopologiaImportada
from Recursos.generarTopologiaArbol import generarArbol
from Recursos.generarTopologiaAnillo import generarAnillo
from Recursos.generarTopologiaMalla import generarMalla
from Recursos.generarTopologiaLineal import generarLineal
import Recursos.funcionEnviarMail as mail

console = Console()

headers = {
            "Content-Type": "application/json",
            'X_APP_IDENTIFIER': "0a8cebdb56fdc2b22590690ebe5a3e2b",
           }

def crearSlice(usuarioLog, endpointBase):
    title = "Seleccione un tipo de topología:"
    choicesCrear = ["1. Predeterminado", "2. Personalizado", "3. Importar topología", "**Regresar**"]
    opcion = questionary.select(title, choices=choicesCrear).ask()    
    if (opcion == "**Regresar**"):
        return
    else:
        if(opcion == "1. Predeterminado"):
            topologiaPredeterminada(usuarioLog, endpointBase)
        elif(opcion == "2. Personalizado"):
            topologiaPersonalizada(usuarioLog, endpointBase)
        elif(opcion=="3. Importar topología"):
            importarTopologia(usuarioLog, endpointBase)

def importarTopologia(usuarioLog, endpointBase):
    filename = questionary.path("Seleccionar archivo para importar: ").ask()
    try:
        with open(filename, "r") as archivo:
            print(Fore.CYAN+"Cargando previsualización...")
            time.sleep(1)
            jsonfile = graficarTopologiaImportada(json.load(archivo))
            confirmationCrear = questionary.confirm("¿Desea crear este slice?").ask()
            if(confirmationCrear):
                fecha_actual = datetime.datetime.now()
                opcionesAZ = ["1. Openstack - Golden Zone", "2. Linux - Silver Zone"]
                plataformaElegida = questionary.select("Seleccione una zona de disponibilidad: ", choices=opcionesAZ).ask()
                jsonfile['fecha'] = fecha_actual.strftime("%d/%m/%Y")
                if(plataformaElegida == opcionesAZ[0]):
                    jsonfile["AZ"] = "Golden Zone"  
                else:
                    jsonfile["AZ"] = "Silver Zone"  
                validarSliceCrearRecursos(usuarioLog, endpointBase, jsonfile)
            else:
                crearSlice(usuarioLog, endpointBase)
    except FileNotFoundError:
        print(Fore.RED+"El archivo no se encontró")
    except IOError:
        print(Fore.RED+"Ocurrió un error al intentar abrir el archivo")
    crearSlice(usuarioLog, endpointBase)

def topologiaPredeterminada(usuarioLog, endpointBase):
    choicesPredeterminada = ["1. Malla","2. Árbol","3. Anillo","4. Lineal","5. Salir"]
    title = "Seleccione el tipo de topología:"
    opcion = questionary.select(title, choices=choicesPredeterminada).ask()
    if(opcion =="5. Salir"):
        crearSlice(usuarioLog, endpointBase)
    else: 
        listaEnlaces, listaNodos = [], []
        if(opcion=="1. Malla"):
            while not (numNodos := questionary.text("Ingrese el número de nodos").ask().strip()):
                print(Fore.YELLOW + "Debe definir un número de nodos")
            titulo = "Malla con "+numNodos
            listaEnlaces, listaNodos = generarMalla(int(numNodos))
        elif(opcion=="2. Árbol"):
            while not (niveles := questionary.text("Ingrese el número de niveles del árbol").ask().strip()):
                print(Fore.YELLOW + "Debe definir un número de niveles")
            while not (hijos := questionary.text("Ingrese el número de hijos por nodo").ask().strip()):
                print(Fore.YELLOW + "Debe definir un número de hijos por nodo")
            titulo = "Arbol nivel "+niveles+" con "+hijos+" hijos por nodo"
            listaEnlaces, listaNodos = generarArbol(int(hijos), int(niveles))
        elif(opcion=="3. Anillo"):
            while not (numNodos := questionary.text("Ingrese el número de nodos").ask().strip()):
                print(Fore.YELLOW + "Debe definir un número de nodos")
            titulo = "Anillo con "+numNodos
            listaEnlaces, listaNodos = generarAnillo(int(numNodos))
        elif(opcion=="4. Lineal"):
            while not (numNodos := questionary.text("Ingrese el número de nodos").ask().strip()):
                print(Fore.YELLOW + "Debe definir un número de nodos")
            titulo = "Lineal con "+numNodos
            listaEnlaces, listaNodos = generarLineal(int(numNodos))
        confirmation = questionary.confirm("¿Desea tener una vista previa?").ask()

        if confirmation:
            graficarTopologia(titulo, listaNodos, listaEnlaces)
        response = requests.get(url = endpointBase+"/imagenes/listar", 
                                        headers = headers)
        imagenes = response.json()['result']
        imagenesOpciones = [imagen['nombre'] for imagen in imagenes]
        print(Fore.CYAN+"================= IMÁGENES =================")
        imagenChoosedName = questionary.select("Seleccione una imagen: ", choices=imagenesOpciones).ask()

        response = requests.get(url = endpointBase+"/flavors/listar", 
                                        headers = headers)
        flavors = response.json()['result']
        print(Fore.CYAN+"================= FLAVORS =================")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("N°",justify="center")
        table.add_column("Nombre", justify="center")
        table.add_column("RAM (MB)",justify="center")
        table.add_column("Disco (GB)", justify="left")
        table.add_column("N° Cores", justify="lef")
        index = 1
        for flavor in flavors:
            nombre = flavor['nombre']
            ram = flavor['ram']
            disk = flavor['disk']
            cpus = flavor['cpu']
            table.add_row(str(index), nombre, str(ram), str(disk), str(cpus))
            index+=1
        console.print(table)
        flavorName = [flavor['nombre'] for flavor in flavors]
        flavorChoosedName = questionary.select("Seleccione un flavor: ", choices=flavorName).ask()
        flavor_seleccionado = [flavor for flavor in flavors if flavor["nombre"] == flavorChoosedName][0]
        imagen_seleccionado = [imagen for imagen in imagenes if imagen["nombre"] == imagenChoosedName][0]
        VMsDetalladas = []
        for vm_name in listaNodos:
            VMsDetalladas.append(recurso.VM(vm_name, "", flavor_seleccionado['ram'], flavor_seleccionado['cpu'], flavor_seleccionado['disk'] , imagen_seleccionado['filename'] ,imagen_seleccionado['idglance'], flavor_seleccionado['idflavorglance']).to_dict())
        
        while not (nombre := questionary.text("Ingrese un nombre para su slice").ask().strip()):
            print(Fore.YELLOW + "Su slice debe tener un nombre")
        
        confirmationCrear = questionary.confirm("¿Desea crear este slice?").ask()
        if(confirmationCrear):
            fecha_actual = datetime.datetime.now()
            opcionesAZ = ["1. Openstack - Golden Zone", "2. Linux - Silver Zone"]
            plataformaElegida = questionary.select("Seleccione una zona de disponibilidad: ", choices=opcionesAZ).ask()
            if(plataformaElegida == opcionesAZ[0]):
                slice = {"vms": VMsDetalladas, "enlaces":listaEnlaces, "nombre":nombre, "fecha":fecha_actual.strftime("%d/%m/%Y"), "AZ": "Golden Zone"}  
            else:
                slice = {"vms": VMsDetalladas, "enlaces":listaEnlaces, "nombre":nombre, "fecha":fecha_actual.strftime("%d/%m/%Y"), "AZ": "Silver Zone"}  
            validarSliceCrearRecursos(usuarioLog, endpointBase, slice)
        else:
            crearSlice(usuarioLog, endpointBase)

def validarDisponibilidadServidor(usuarioLog, endpointBase):
    response = requests.get(url = endpointBase+"/disponible/"+str(usuarioLog.idUser), 
                                headers = headers)
    if(response.status_code == 200):
        respuestaServer = response.json()['result']
        if(respuestaServer == "Disponible"):
            print("Disponible")
            return True
        elif(respuestaServer == "Ocupado"):
            print("Ocupado")
            confirmReintentar = questionary.confirm("Servidor temporalmente ocupado, ¿reintentar nuevamente?...").ask()
            if(confirmReintentar):
                time.sleep(2)
                validarDisponibilidadServidor(usuarioLog, endpointBase)
            else:
                return False
    else:
        confirmReintentar = questionary.confirm("Problema con el servidor, reintentando").ask()
        if(confirmReintentar):
            time.sleep(1)
            validarDisponibilidadServidor(usuarioLog, endpointBase)
        else:
            return False

def crearRecursos(usuarioLog, endpointBase, data):
    passwd = questionary.password("Digite su contraseña para confirmar creación: ").ask()

    responseRecursos = requests.post(url=endpointBase+"/validacionRecursos/"+str(usuarioLog.idUser), 
                                     headers=headers, data=json.dumps(data))
    if(responseRecursos.status_code==200):
        resultRecursos = responseRecursos.json()['result']
        if(resultRecursos=="exito"):
            print(Fore.GREEN+"Se cuentan con recursos suficiente para crear este slice")
            print(Fore.GREEN+"Desplegando slice en la zona de disponibilidad elegida...")
            
            responseSliceCrear = requests.post(url = endpointBase+"/slice/crear/"+str(usuarioLog.idUser)+"/"+usuarioLog.username+"/"+passwd+"/"+data['nombre'], 
                                headers = headers, data=json.dumps(data))
            if(responseSliceCrear.status_code == 200):
                resultSliceCrear = responseSliceCrear.json()['result']
                if(resultSliceCrear != None):
                    print(Fore.GREEN+"Slice creado exitosamente, registrando en Base de datos...")
                    dataRegistrar = {"result":resultSliceCrear, "data":data}
                    responseGuardarBD = requests.post(url = endpointBase+"/slice/guardarBD/"+str(usuarioLog.idUser)+"/"+data['nombre'], 
                                headers = headers, data=json.dumps(dataRegistrar))
                    if(responseGuardarBD.status_code == 200 and responseGuardarBD.json()['result'] == "exito"):
                        print(Fore.GREEN+"Slice registrado exitosamente!!")
                    else:
                        responseGuardarBD = requests.post(url = endpointBase+"/slice/guardarBD/"+str(usuarioLog.idUser)+"/"+data['nombre'], 
                                headers = headers, data=json.dumps(dataRegistrar))
                    print(Fore.YELLOW+"Actualizando recursos...")
                    requests.get(url=endpointBase+"/recursos/updateDisponibles", headers=headers)
                    print(Fore.GREEN+"Recursos actualizados con éxito")
                    return True
                else:
                    print(Fore.RED+"Problema al crear el slice en "+data['AZ'])
                    return False
            else:
                print(Fore.RED+"Problema con el servidor")
        else:
            print(Fore.RED+resultRecursos)
    else:
        print(Fore.RED+"Problema con el servidor")  

def topologiaPersonalizada(usuarioLog, endpointBase):
    print(Fore.CYAN+"Usted está empezando con la creación de su topología...")
    print(Fore.CYAN+"Agregue al menos 2 VM y 1 enlace")
    print(Fore.CYAN+"Añada sus Máquinas virtuales...")
    listaVMs = []
    listaVMs.append(recurso.agregarVM(endpointBase, listaVMs))
    listaVMs.append(recurso.agregarVM(endpointBase, listaVMs))
    while(True):
        confirmVM = questionary.confirm("¿Desea añadir otra VM?").ask()
        if(confirmVM):
            listaVMs.append(recurso.agregarVM(endpointBase, listaVMs))
        else:
            break
    listaEnlaces = []
    listaEnlaces.append(recurso.generarEnlace(listaVMs, listaEnlaces))
    while(True):
        confirmLink = questionary.confirm("¿Desea añadir otro enlace?").ask()
        if(confirmLink):
            vm1, vm2 = recurso.generarEnlace(listaVMs, listaEnlaces)
            if ((vm1 is not None) and (vm2 is not None)):
                listaEnlaces.append((vm1, vm2))
            else:
                continue
        else:
            dispositivosLibres = recurso.dispositivosNoConectados(listaVMs, listaEnlaces)
            if (len(dispositivosLibres)==0):
                break
            else:
                print(Fore.YELLOW+"No ha conectado todos sus dispositivos")
                vms_sin_conectar = dispositivosLibres
                for vm_nombre in vms_sin_conectar:
                    vm_alias = next(vm['alias'] for vm in listaVMs if vm['nombre'] == vm_nombre)
                    print(Fore.YELLOW + "Nodo sin conectar:", vm_alias)
                continue
    confirmation = questionary.confirm("¿Desea tener una vista previa?").ask()
    listaVMsNombres = []
    for vm in listaVMs:
        listaVMsNombres.append(vm['nombre'])
    if confirmation:
        graficarTopologia("Diagrama Topología", listaVMsNombres,listaEnlaces)
    fecha_actual = datetime.datetime.now()
    while not (nombre := questionary.text("Ingrese un nombre para su slice").ask().strip()):
        print(Fore.YELLOW + "Su slice debe tener un nombre")

    confirmationCrear = questionary.confirm("¿Desea crear este slice?").ask()
    if(confirmationCrear):
        opcionesAZ = ["1. Openstack - Golden Zone", "2. Linux - Silver Zone"]
        plataformaElegida = questionary.select("Seleccione una zona de disponibilidad: ", choices=opcionesAZ).ask()
        if(plataformaElegida == opcionesAZ[0]):
            slice = {"vms": listaVMs, "enlaces":listaEnlaces, "nombre":nombre, "fecha":fecha_actual.strftime("%d/%m/%Y"), "AZ": "Golden Zone"}  
        else:
            slice = {"vms": listaVMs, "enlaces":listaEnlaces, "nombre":nombre, "fecha":fecha_actual.strftime("%d/%m/%Y"), "AZ": "Silver Zone"}  
        validarSliceCrearRecursos(usuarioLog, endpointBase, slice)
    else:
        crearSlice(usuarioLog, endpointBase)

def validarSliceCrearRecursos(usuarioLog, endpointBase, slice):
    if(validarDisponibilidadServidor(usuarioLog, endpointBase)):
        print(Fore.GREEN+"Servidor disponible, consultando recursos...")
        if(crearRecursos(usuarioLog, endpointBase, slice)):
            response = requests.get(url = endpointBase+"/vm/listar/"+str(slice['nombre']), 
                                        headers = headers)
            result = response.json()['result']
            nombres_graficar = []
            for vm in slice["vms"]:
                if not vm["alias"]:
                    nombres_graficar.append(vm["nombre"])
            rutaImagen = graficarTopologia("Slice: "+" "+slice['nombre']+" Fecha: "+slice['fecha'], nombres_graficar, slice['enlaces'], True, slice['nombre'])
            print(Fore.GREEN+"Enviando correo con credenciales y topología...")
            try:
                plataformaDespliegue = slice['AZ']
                azs = ["Golden Zone", "Silver Zone"]
                if(plataformaDespliegue == azs[0]):
                    # GUARDAR OPENSTACK
                    mail.send_user_slice("[OLIMPUS] Nuevo Slice Creado", usuarioLog.correo, usuarioLog.username, result,rutaImagen)
                else:
                    mail.send_accesos_linux("[OLIMPUS] Nuevo Slice Creado", usuarioLog.correo, usuarioLog.username, result,rutaImagen, "ManualDeAcceso.pdf")
            except Exception as e:
                print(f"Error: {e}")
            exportarConfirm = questionary.confirm("¿Exportar esta topología?").ask()
            if(exportarConfirm):
                nombreFile = questionary.text("Ingrese el nombre del archivo (sin extensión): ").ask()
                with open(nombreFile+".json", "w") as json_file:
                    json.dump(slice, json_file)
    else:
        crearSlice(usuarioLog, endpointBase)