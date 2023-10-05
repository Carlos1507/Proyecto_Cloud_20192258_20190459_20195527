import questionary, requests, json, sys, hashlib
from colorama import Fore, Style, init
global usuarioBD
global usuarioLog
class User:
    def __init__(self, idUser, username, correo, rol, eligioAZs):
        self.idUser = idUser
        self.username = username
        self.correo = correo
        self.rol = rol
        self.eligioAZs = eligioAZs

def autorizacion(endpointBase):
    username = questionary.text("Usuario: [digite 0 aquí para salir]").ask()
    username = username.strip()
    if(username !="0"):
        hash_sha512 = hashlib.sha512()
        passw = questionary.password("Contraseña: ").ask()
        hash_sha512.update(passw.encode("utf-8"))
        print("Validando...")
        response = requests.post(url = endpointBase+"/validarPOST", 
                                headers = {"Content-Type": "application/json"}, 
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
                                  usuarioBD['result'][5], usuarioBD['result'][4])
                
                return usuarioLog
        else:
            print("Error de autenticación")
            autorizacion()
    else:
        sys.exit(0)