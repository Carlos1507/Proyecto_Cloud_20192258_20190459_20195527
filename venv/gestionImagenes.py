import questionary, requests, json
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init
from enviarArchivoSCP import enviarSCP
console = Console()

longitudLinea = 30
def gestorImagenes():
    opcionesMenuImagenes = ["1. Agregar imagen", "2. Listar imágenes", "3. Eliminar imagen","4. Regresar"]
    opcion = questionary.select("Submenú Gestión de Imágenes: ", choices=opcionesMenuImagenes).ask()  
    if(opcion=="4. Regresar"):
        print("Saliendo del submenú de imágenes...")
        return
    else:
        if(opcion=="1. Agregar imagen"):
            agregarImagen()
        elif(opcion=="2. Listar imágenes"):
            listarImagenes()
        else:
            eliminarImagen()
    
def agregarImagen():
    filename = questionary.path("Seleccionar archivo: ").ask()
    try:
        with open(filename, "r") as archivo:
            enviarSCP(filename, 'ubuntu', '10.20.10.149', '/home/ubuntu', 5800, 'headnode')
            response = requests.post(url = "http://127.0.0.1:8000/agregarImagen", 
                                        headers = {"Content-Type": "application/json"}, data=json.dumps({"nombre":filename}))
            if(response.status_code==200 and response.json()['result']=="Correcto"):
                print(Fore.GREEN+"Imagen agregada exitosamente")
            else:
                print(Fore.RED+"Error en el servidor")
    except FileNotFoundError:
        print(Fore.RED+"El archivo no se encontró")
    except IOError:
        print(Fore.RED+"Ocurrió un error al intentar abrir el archivo")
    gestorImagenes()

def eliminarImagen():
    response = requests.get(url = "http://127.0.0.1:8000/allImagenes", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        imagenes = response.json()['result']
        imagenesOpciones = [imagen[1] for imagen in imagenes]
        imagenNombre = questionary.rawselect("Elija una imagen a eliminar: ", choices=imagenesOpciones).ask()
        idEliminar = [imagen[0] for imagen in imagenes if imagen[1] == imagenNombre] [0]
        resultadoEliminar = requests.get(url = "http://127.0.0.1:8000/eliminarImagen/"+str(idEliminar), 
                                         headers = {"Content-Type": "application/json"})
        if(resultadoEliminar.status_code==200 and resultadoEliminar.json()["result"] == "Correcto"):
            print(Fore.GREEN+"Imagen Eliminado Correctamente")
        else:
            print(Fore.RED+"Hubo un problema al eliminar, intente nuevamente")
    else:
        print(Fore.RED + "Error en el servidor")
    gestorImagenes()

def listarImagenes():
    response = requests.get(url = "http://127.0.0.1:8000/allImagenes", 
                                headers = {"Content-Type": "application/json"})
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
    gestorImagenes()