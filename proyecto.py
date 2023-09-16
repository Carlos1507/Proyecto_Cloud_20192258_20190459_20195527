# Definición de librerías y constantes
import http.client as httplib
import json

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
    def postReq(self, data):
        ret = self.rest_call('POST', "", data)
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
a = APIServ("127.0.0.1")
def autorizacion():
    user = input("Usuario: ")
    passw = input("Contraseña: ")
    print(f"Usuario: {user} Contraseña: {passw}")
    print("Validando...")
    resultado = pusher.getReq("imprimir")
    

# Definición de funciones adicionales a implementar:
def conexionBD():
    pass
def menu():
    opcion = ""
    print("What would you like to do today?")
    return opcion
# Función principal
if __name__ == "__main__":    
    pusher = APIServ("127.0.0.1")
    print("Welcome to the Cloud Service: CGC (The Cloud Gods Carry)")
    print("Please enter your credentials to log in to the system: ")
    usuario = autorizacion()
   # menu(usuario)