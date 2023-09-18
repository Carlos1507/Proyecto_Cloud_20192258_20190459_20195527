# Definición de librerías y constantes
import http.client as httplib
import json
import time
import getpass

headers = {'Content-type': 'application/json'}
# Definición de las clases a implementar (elementos):
class virtualMachine:
    pass
class slice:
    pass
class user:
    pass
# Conexión WebService NodeJS
endpoint="http://127.0.0.1:3000/"
class APIServ(object):
    def __init__(self, server):
        self.server = server
    def postReq(self, subruta, data):
        ret = self.rest_call('POST', subruta, data)
        return ret[0]==200
    def getReq(self, subruta):
        ret = self.rest_call('GET', subruta)
        return ret[0]==200
    def rest_call(self, action, subruta, data=""):
        path = endpoint+subruta
        conn = httplib.HTTPConnection(self.server, 3000)
        if action == 'POST':
            body = json.dumps(data)
            conn.request(action, path, body, headers)
        conn.request(action, path, "", headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print(ret)
        conn.close()
        return ret

# Definición de los módulos a implementar:
def autorizacion():
    user = input("Usuario: ")
    passw = ""
    try:
        passw = getpass.getpass("Contraseña: ")
    except Exception as err:
        print("Error: " + err)    
    print("Validando...")
    time.sleep(2)
  #  resultado = pusher.getReq("imprimir")
  #  valido = pusher.postReq("validarPOST", {"user": user, "password": passw})
    if(user == "diego" and passw =="root"):
        return True
    else:
        print("Credenciales incorrectas")
        autorizacion()
# Funciones del menú
# Crear Slice
def topologiaPredeterminada():
    print("Seleccione el tipo de topología: \n\t1. Malla\n\t2. Árbol\n\t3. Anillo\n\t4. Lineal")
def topologiaPersonalizada():
    pass
def crearSlice():
    print("Tipo de topología:\n\t1. Predeterminado\n\t2. Personalizado")
    topologia = input("\tOpción: ")
    if(topologia == "1"):
        topologiaPredeterminada()
    elif(topologia == "2"):
        topologiaPersonalizada()
    else:
        crearSlice()
# Listar Slice
def listarSlice():
    pass
# Definir zonas de disponibilidad
def zonasDisponibilidad():
    print("Seleccione la configuación de zonas de disponibilidad")
    print("Opción 1: \n\tAZ1: Worker1\tAZ2:Worker2\tAZ3:Worker3")
    print("Opción 2: \n\tAZ1: Worker1 & Worker2\tAZ2:Worker3")
    print("Opción 3: \n\tAZ1: Worker1 & Worker2 & Worker3")
    

# Definición de funciones adicionales a implementar:
def menu():
    opcion = ""
    print("What would you like to do today?")
    print("1. Crear Slice")
    print("2. Listar Slices")
    print("3. Definir zona de disponibilidad")
    opcion = input("Seleccione una opción: ")
    if(opcion =="1"):
        crearSlice()
    elif(opcion =="2"):
        listarSlice()
    elif(opcion =="3"):
        zonasDisponibilidad()        
    else:
        menu()
def seleccionarPlataforma():
    print("Select the platform: ")
    print("1. Linux")
    print("2. OpenStack")
    opcionPlataforma = input("Option: ")
    if(opcionPlataforma =="1" or opcionPlataforma=="2"):
        return opcionPlataforma
    else:
        seleccionarPlataforma()
# Función principal
if __name__ == "__main__":    
    pusher = APIServ("127.0.0.1")
    print("Welcome to the Cloud Service: CCG (The Cloud Computing Gods)")
    print("Please enter your credentials to log in to the system: ")
    valido = autorizacion()
    opcionPlataforma = seleccionarPlataforma()
    opcion = menu()


a = "variable"