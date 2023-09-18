# Definición de librerías y constantes
import http.client as httplib
import json
import time
import getpass
import sys
# Variables globales
global usuarioLog

headers = {'Content-type': 'application/json; charset=utf-8'}
# Definición de las clases a implementar (elementos):
class virtualMachine:
    pass
class slice:
    pass
class User:
    def __init__(self, nombre, username, correo, rol, eligioAZs=0, eleccionAZs=""):
        self.nombre = nombre
        self.username = username
        self.correo = correo
        self.rol = rol
        self.eligioAZs = eligioAZs
        self.eleccionAZs = eleccionAZs
        
# Conexión WebService NodeJS
endpoint="http://127.0.0.1:3000/"
class APIServ(object):
    def __init__(self, server):
        self.server = server
    def postReq(self, subruta, data):
        ret = self.rest_call('POST', subruta, data)
        return ret
    def getReq(self, subruta):
        ret = self.rest_call('GET', subruta)
        return ret
    def rest_call(self, action, subruta, data=""):
        path = endpoint+subruta
        conn = httplib.HTTPConnection(self.server, 3000)
        if action == 'POST':
            body = json.dumps(data)
            conn.request(action, path, body, headers)
        elif action == 'GET':
            conn.request(action, path, "", headers)
        response = conn.getresponse()
        status = response.status
        reason = response.reason
        content = json.loads(response.read().decode("utf-8"))
      #  print(f"Status: {status} - {reason}")
      #  print(f"Response Data: {content}")
        ret = (response.status, response.reason, content)
        conn.close()
        return ret

# Definición de los módulos a implementar:
def autorizacion():
    username = input("Usuario: ")
    passw = ""
    try:
        passw = getpass.getpass("Contraseña: ")
    except Exception as err:
        print("Error: " + err)
    print("Validando...")
    time.sleep(2)
  #  resultado = pusher.getReq("imprimir")
    usuarioBD = pusher.postReq("validarPOST", {"username": username, "password": passw})[2]
    if(len(usuarioBD) != 0):
        usuarioBD = usuarioBD[0]
        if(usuarioBD['username']=="diego123"):
            usuarioLog = User(usuarioBD['nombres']+" "+usuarioBD['apellidos'],usuarioBD['username'],usuarioBD['correo'],"Usuario",0)
        else:
            usuarioLog = User(usuarioBD['nombres']+" "+usuarioBD['apellidos'],usuarioBD['username'],usuarioBD['correo'],"Administrador",0)
        return usuarioLog
    else:
        print("Credenciales incorrectas")
        autorizacion()
# Funciones del menú
# Crear Slice
def topologiaPredeterminada():
    print("Seleccione el tipo de topología: \n\t1. Malla\n\t2. Árbol\n\t3. Anillo\n\t4. Lineal\n\t5. Salir")
    opcion=input("Opción: ")
    if(opcion=="1"):
        pass
    elif(opcion=="2"):
        pass
    elif(opcion=="3"):
        pass
    elif(opcion=="4"):
        pass
    elif(opcion=="5"):
        crearSlice()
    else:
        topologiaPredeterminada()
def topologiaPersonalizada():
    numberVMs = input("Indique el número de VMs a crear: ")

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
# Listar Slice
def listarSlice():
    if(usuarioLog.rol=="Usuario"):
        ListasAlumnos = [['1', 'Prueba', "11/07/2023", 4, 5, "Si"], 
                 ['2', 'Entorno1', "19/07/2023", 8, 9, "No"],
                 ['3', 'Simulación', "4/08/2023", 6, 10, "Si"]]
        Tabla = """
        +----------------------- Slices personales creados ---------------------+
        +-----------------------------------------------------------------------+
        | N°   Nombre        Fecha        Número VMs  Número Enlaces    Activo  |
        |-----------------------------------------------------------------------|
        {}
        +-----------------------------------------------------------------------+
        """
        formatted_rows = []
        for i, fila in enumerate(ListasAlumnos):
            if i == 0:
                formatted_rows.append("| {:<3} {:<14} {:<12} {:<12} {:<17} {:<6} |".format(*fila))
            else:
                formatted_rows.append("\t| {:<3} {:<14} {:<12} {:<12} {:<17} {:<6} |".format(*fila))
        Tabla = Tabla.format('\n'.join(formatted_rows))
        print(Tabla)
    else:
        ListasAlumnos = [['1', 'Prueba', "11/07/2023", 4, 5, "Si"], 
                         ['2','VNRT',"7/04/2023",10,20,"Si"], 
                         ['3','Exogeni',"2/01/2023",15,20,"Si"], 
                 ['4', 'Entorno1', "19/07/2023", 8, 9, "No"],
                 ['5', 'Simulación', "4/08/2023", 6, 10, "Si"]]
        Tabla = """
        +---------------------- Todos los Slices existentes --------------------+
        +-----------------------------------------------------------------------+
        | N°   Nombre        Fecha        Número VMs  Número Enlaces    Activo  |
        |-----------------------------------------------------------------------|
        {}
        +-----------------------------------------------------------------------+
        """
        formatted_rows = []
        for i, fila in enumerate(ListasAlumnos):
            if i == 0:
                formatted_rows.append("| {:<3} {:<14} {:<12} {:<12} {:<17} {:<6} |".format(*fila))
            else:
                formatted_rows.append("\t| {:<3} {:<14} {:<12} {:<12} {:<17} {:<6} |".format(*fila))
        Tabla = Tabla.format('\n'.join(formatted_rows))
        print(Tabla)
# Definir zonas de disponibilidad
def zonasDisponibilidad():
    if (usuarioLog.eligioAZs == 0):
        print("Seleccione la configuación de zonas de disponibilidad")
        print("*** Esta acción solo se puede realizar 1 sola vez ***")
        print("Opción 1: \n\tAZ1: Worker1\tAZ2:Worker2\tAZ3:Worker3")
        print("Opción 2: \n\tAZ1: Worker1 & Worker2\tAZ2:Worker3")
        print("Opción 3: \n\tAZ1: Worker1 & Worker2 & Worker3")
        opcion = input("Opción: ")
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
# Definición de funciones adicionales a implementar:
def menu():
    opcion = ""
    print("¿Qué acción desea hacer hoy?")
    print("1. Crear Slice")
    print("2. Listar Slices")
    print("3. Definir zona de disponibilidad")
    print("4. Cerrar Sesión")
    opcion = input("Seleccione una opción: ")
    if(opcion =="1"):
        crearSlice()
    elif(opcion =="2"):
        listarSlice()
    elif(opcion =="3"):
        zonasDisponibilidad()       
    elif(opcion =="4"):
        usuarioLog = None
        print("*** Muchas gracias por usar nuestro sistema ***")
        sys.exit(0)
    else:
        print("--- Elija una opción válida ---")
        menu()
def seleccionarPlataforma():
    print("Seleccione la plataforma: \n\t1. Linux\t2. OpenStack")
    opcionPlataforma = input("Opción: ")
    if(opcionPlataforma =="1" or opcionPlataforma=="2"):
        return opcionPlataforma
    else:
        print("--- Elija una opción válida ---")
        seleccionarPlataforma()
# Función principal
if __name__ == "__main__":    
    pusher = APIServ("127.0.0.1")
    print("Bienvenido al Servicio Cloud: CCG (The Cloud Computing Gods)")
    print("Por favor ingrese sus credenciales para iniciar sesión en el sistema: ")
    usuarioLog = autorizacion()
    print(f"Bienvenido {usuarioLog.nombre}")
    opcionPlataforma = seleccionarPlataforma()
    opcion = menu()