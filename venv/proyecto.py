# Definición de librerías y constantes
import questionary, json, sys, requests, hashlib
from colorama import Fore, Style, init
from modulo_autorizacion import autorizacion as auth
from menuPrincipal import menu
init(autoreset=True)

# Variables globales
global usuarioLog
global imagenes 
longitudLinea = 30
imagenesNombres = ["cirros-image.img", "ubuntu-iso-20.04.iso"]
headers = {'Content-type': 'application/json; charset=utf-8'}
        
# Definición de los módulos a implementar:
# Crear Slice
def topologiaPredeterminada():
    print("Seleccione el tipo de topología: \n\t1. Malla\n\t2. Árbol\n\t3. Anillo\n\t4. Lineal\n\t5. Salir")
    opcion=input("\t**Opción: ")
    if(opcion=="1"):
        eleccionAZ()
    elif(opcion=="2"):
        eleccionAZ()
    elif(opcion=="3"):
        eleccionAZ()
    elif(opcion=="4"):
        eleccionAZ()
    elif(opcion=="5"):
        crearSlice()
    else:
        topologiaPredeterminada()
def topologiaPersonalizada():
    while(True):
        print("1. Añadir máquina virtual (VM)")
        print("2. Añadir enlace")
def eleccionAZ():
    print("--- AZ elegida: ---")
    print(usuarioLog.eleccionAZs)
    az= input("Seleccione el AZ para desplegar el slice")
    print("--- Despliegue exitoso ---")
    menu()
def crearSlice():
    if(usuarioLog.eligioAZs==1):
        print("Tipo de topología:\n\t1. Predeterminado\n\t2. Personalizado\n\t3. Salir")
        topologia = input("\tOpción: ")
        if(topologia == "1"):
            topologiaPredeterminada()
        elif(topologia == "2"):
            topologiaPersonalizada()
        elif(topologia == "3"):
            menu()
        else:
            print("--- Elija una opción válida ---")
            crearSlice()
    else:
        zonasDisponibilidad()
# Definir zonas de disponibilidad
def zonasDisponibilidad():
    if (usuarioLog.eligioAZs == 0):
        print("Seleccione la configuación de zonas de disponibilidad")
        print("*** Esta acción solo se puede realizar 1 sola vez ***")
        print("Opción 1: \n\tAZ1: Worker1\tAZ2:Worker2\tAZ3:Worker3")
        print("Opción 2: \n\tAZ1: Worker1 & Worker2\tAZ2:Worker3")
        print("Opción 3: \n\tAZ1: Worker1 & Worker2 & Worker3")
        opcion = input("\t**Opción: ")
        if (opcion == "1"):
            usuarioLog.eligioAZs = 1
            usuarioLog.eleccionAZs = "AZ1: Worker1\tAZ2:Worker2\tAZ3:Worker3"
            print("--------------------------------------")
            menu()
        elif (opcion == "2"):
            usuarioLog.eligioAZs = 1
            usuarioLog.eleccionAZs = "AZ1: Worker1 & Worker2\tAZ2:Worker3"
            print("--------------------------------------")
            menu()
        elif (opcion == "3"):
            usuarioLog.eligioAZs = 1
            usuarioLog.eleccionAZs = "AZ1: Worker1 & Worker2 & Worker3"
            print("--------------------------------------")
            menu()
        else:
            print("--- Elija una acción válida ---")
            zonasDisponibilidad()
    else:
        print("--- La zona ya ha sido seleccionada ---")
        print(usuarioLog.eleccionAZs)
        menu()
def agregarImagenes():
    filename = input("Seleccionar archivo: ")
    imagenesNombres.append(filename)
    print("-"*longitudLinea)
    menu()
def listarImagenes():
    for i in range(1,len(imagenesNombres)+1):
        print(str(i)+". "+imagenesNombres[i-1])
    print("-"*longitudLinea)
    borrarImagenes =input("¿Borrar imágenes? (S/N): ")
    if(borrarImagenes=="S" or borrarImagenes=="s"):
        numImagen = input("Seleccione el número de imagen a borrar: ")
        try:
            numImagen = int(numImagen)
            if(numImagen>0 and numImagen<=len(imagenesNombres)):
                imagenesNombres.remove(imagenesNombres[numImagen-1])
                print("Imagen eliminada exitosamente")
                imagenes()
            else:
                print(numImagen)
        except Exception as err:
            print("Error: " + err)
            print("Debe seleccionar un número válido")
            imagenes()
        finally:
            print("Error")
def imagenes():
    print("1. Agregar imagen")
    print("2. Listar imágenes")
    print("3. Salir")
    opcion = input("\t**Opción: ")
    if(opcion =="1"):
        agregarImagenes()
    elif(opcion =="2"):
        listarImagenes()
    elif(opcion=="3"):
        menu()
    else:
        print("--- Elija una acción válida ---")
        imagenes()

# Definición de funciones adicionales a implementar:
def seleccionarPlataforma():
    opcionPlataforma = questionary.select("Seleccione la plataforma:", choices=["1. Linux", "2. OpenStack", "0. Salir"]).ask()
    if(opcionPlataforma == "1. Linux" or opcionPlataforma=="2. OpenStack"):
        return opcionPlataforma
    else:
        print(Fore.RED+"--- Fin del programa ---")
        sys.exit(0)

if __name__ == "__main__":
    while True:
        print("Bienvenido al Servicio Cloud: CCG (The Cloud Computing Gods)")
        print("Por favor ingrese sus credenciales para iniciar sesión en el sistema: ")
        usuarioLog = auth()
        if usuarioLog == None:
            continue
        print(Fore.CYAN + f"Bienvenido {'Operador:' if usuarioLog.rol == 1 else 'Usuario:'} {usuarioLog.username}")
        opcionPlataforma = seleccionarPlataforma()
        opcion = menu(usuarioLog)
        if opcion is None:
            print("Sesión terminada. Vuelva a iniciar sesión")
        else:
            break