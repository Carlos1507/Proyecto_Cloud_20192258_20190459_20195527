# Definición de librerías y constantes
from colorama import Fore, Style, init
from modulo_autorizacion import autorizacion
from menuPrincipal import menu
# Inicializar color
init(autoreset=True)
# Variables globales
global usuarioLog

if __name__ == "__main__":
    endpointBase = "http://10.20.10.221:8000"
    ruta_llave = "venv/headnode"
    gateway_ip = "10.20.10.221"
    while True:
        print(Fore.CYAN+"Bienvenido al Servicio Cloud: The Cloud Computing Olimpus")
        print(Fore.CYAN+"Por favor ingrese sus credenciales para iniciar sesión en el sistema: ")
        usuarioLog = autorizacion(endpointBase)
        if usuarioLog == None:
            continue
        print(Fore.CYAN + f"Bienvenido {'Operador:' if usuarioLog.rol == 1 else 'Usuario:'} {usuarioLog.username}")
        opcion = menu(usuarioLog, endpointBase)
        if opcion is None: print("Sesión terminada. Vuelva a iniciar sesión")
        else: break