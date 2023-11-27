import questionary, requests, json, os
from rich.console import Console
from rich.table import Table
import Recursos.funcionEjecutarComandoRemoto as ejecutarComando
from colorama import Fore, Style, init
from Recursos.funcionEnviarArchivoSCP import enviarSCP
from Recursos.funcionEjecutarComandoRemoto import execRemoto
import Operador.moduloOperadorGestionFlavors as gestionFlavors

console = Console()
headers = {
            "Content-Type": "application/json",
            'X_APP_IDENTIFIER': "0a8cebdb56fdc2b22590690ebe5a3e2b",
           }

longitudLinea = 30
def gestorImagenes(endpointBase):
    opcionesMenuImagenes = ["1. Agregar imagen", "2. Listar imágenes", "3. Eliminar imagen","4. Regresar"]
    opcion = questionary.select("Submenú Gestión de Imágenes: ", choices=opcionesMenuImagenes).ask()  
    if(opcion=="4. Regresar"):
        print("Saliendo del submenú de imágenes...")
        return
    else:
        if(opcion=="1. Agregar imagen"):
            agregarImagen(endpointBase)
        elif(opcion=="2. Listar imágenes"):
            listarImagenes(endpointBase)
        else:
            eliminarImagen(endpointBase)
    
def agregarImagen(endpointBase):
    filename = questionary.path("Seleccionar archivo: ").ask()
    try:
        with open(filename, "r") as archivo:
            enviarSCP(filename, 'ubuntu', "10.20.10.221", '/home/ubuntu/imagenes', 5800, "venv/headkey")
          
            while not (nombreArchivo := questionary.text("Ingrese nombre para su imagen").ask().strip()):
                print(Fore.YELLOW + "El nombre no debe estar vacío")
            
            if(gestionFlavors.gestorImagenesGlance(endpointBase, nombreArchivo, os.path.basename(filename)) == True):
                IDImagencomando = f"openstack image list --name {nombreArchivo} -c ID -f value"
                idImagen = ejecutarComando.execRemoto(IDImagencomando, "10.20.10.221")
                response = requests.post(url = endpointBase+ "/imagen/crear", 
                                            headers = headers, data=json.dumps({"nombre":nombreArchivo,"filename":os.path.basename(filename), "idglance":idImagen}))
                if(response.status_code==200 and response.json()['result']=="Correcto"):
                    print(Fore.GREEN+"Imagen agregada exitosamente")
                else:
                    print(Fore.RED+"Error en el servidor")
            else:
                print(Fore.RED+"Error al guardar imagen")
    except FileNotFoundError:
        print(Fore.RED+"El archivo no se encontró")
    except IOError:
        print(Fore.RED+"Ocurrió un error al intentar abrir el archivo")
    gestorImagenes(endpointBase)

def eliminarImagen(endpointBase):
    response = requests.get(url = endpointBase+"/imagenes/listar", 
                                headers = headers)
    if(response.status_code == 200):
        imagenes = response.json()['result']
        imagenesOpciones = [imagen['nombre'] for imagen in imagenes]
        imagenChoosedName = questionary.rawselect("Elija una imagen a eliminar: ", choices=imagenesOpciones).ask()
        imagen_seleccionado = [imagen for imagen in imagenes if imagen["nombre"] == imagenChoosedName][0]
        resultadoEliminar = requests.delete(url = endpointBase+"/imagen/eliminar/"+str(imagen_seleccionado['idImagenes']), 
                                         headers = headers)
        execRemoto("rm imagenes/"+imagen_seleccionado['filename'], "10.20.10.221")
        if(resultadoEliminar.status_code==200 and resultadoEliminar.json()["result"] == "Correcto"):
            print(Fore.GREEN+"Imagen Eliminado Correctamente")
        else:
            print(Fore.RED+"Hubo un problema al eliminar, intente nuevamente")
    else:
        print(Fore.RED + "Error en el servidor")
    gestorImagenes(endpointBase)

def listarImagenes(endpointBase):
    response = requests.get(url = endpointBase+"/imagenes/listar", 
                                headers = headers)
    if(response.status_code == 200):
        imagenes = response.json()['result']
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("N°", justify="right")
        table.add_column("idImagen",justify="center")
        table.add_column("Nombre Imagen", justify="left")
        for i in range(0,len(imagenes)):
            table.add_row(str(i+1), str(imagenes[i][0]), imagenes[i][1])
        console.print(table)
    else:
        print(Fore.RED + "Error en el servidor")
    gestorImagenes(endpointBase)