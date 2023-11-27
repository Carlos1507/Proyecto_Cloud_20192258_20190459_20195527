import questionary, requests, json, sys, hashlib
from colorama import Fore

global usuarioBD
global usuarioLog
class User:
    def __init__(self, idUser, username, correo, rol):
        self.idUser = idUser
        self.username = username
        self.correo = correo
        self.rol = rol

headers = {
            "Content-Type": "application/json",
            'X_APP_IDENTIFIER': "0a8cebdb56fdc2b22590690ebe5a3e2b",
           }

def autorizacion(endpointBase):
    while not (username := questionary.text("Usuario: [digite 0 aquí para salir]").ask().strip()):
        print(Fore.YELLOW + "El nombre de usuario no debe estar vacío")
    
    username = username.strip()
    if(username !="0"):
        hash_sha512 = hashlib.sha512()
        while not (passw := questionary.password("Contraseña: ").ask().strip()):
            print(Fore.YELLOW + "Debe ingresar una contraseña")
        hash_sha512.update(passw.encode("utf-8"))
        print("Validando...")
        response = requests.post(url = endpointBase+"/usuario/validar", 
                                headers = headers, 
                                data= json.dumps({"username": username, "password": hash_sha512.hexdigest()}))
        if(response.status_code == 200):
            usuarioBD = dict(response.json())
            if (usuarioBD['result'] == "Incorrecto"):
                print(Fore.RED + "Credenciales incorrectas")
                usuarioBD = None
                usuarioLog = None
                return
            else:    
                print(Fore.GREEN + "Logueo exitoso")   
                usuarioLog = User(usuarioBD['result'][0], usuarioBD['result'][1], usuarioBD['result'][3], 
                                  usuarioBD['result'][4])
                
                return usuarioLog
        else:
            print("Error de autenticación")
            autorizacion(endpointBase)
    else:
        sys.exit(0)