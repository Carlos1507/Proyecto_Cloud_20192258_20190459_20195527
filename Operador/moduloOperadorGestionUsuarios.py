import requests, questionary, random, string, re, hashlib, json
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init
from Recursos.funcionEnviarMail import send_email
from servidor import resourceManager

console = Console()

def gestionarUsuarios(usuario, endpointBase):
    opcionesSubMenuUsuarios = ["1. Crear Usuario", "2. Visualizar Usuarios", "3. Eliminar Usuario","4. Regresar"]
    opcion = questionary.select("Submenú Gestión de Usuarios: ", choices=opcionesSubMenuUsuarios).ask()
    if(opcion =="4. Regresar"):
        return
    else:
        if(opcion == "1. Crear Usuario"):
            crearUsuario(usuario, endpointBase)
        elif(opcion == "2. Visualizar Usuarios"):
            listarAllUsers(usuario, endpointBase)
        elif(opcion == "3. Eliminar Usuario"):
            eliminarUsuario(usuario, endpointBase)
    
def crearUsuario(usuario, endpointBase):
    print("Ingrese los siguiente datos: ")
    username = questionary.text("Username:").ask().strip()
    print("Verificando username disponible ...")
    response = requests.get(url = endpointBase+ "/allUsers", headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        # Validando username no repetido y diferente de vacio
        listUsernames = [elemento[1] for elemento in response.json()['result']]
        while(True):
            if(username!=''):
                coincidencia = 0
                for user in listUsernames:
                    if (user == username):
                        coincidencia = 1
                if (coincidencia == 1):
                    print(Fore.RED+"Username ya usado, ingrese otro")
                    username = questionary.text("Username:").ask().strip()
                else:
                    print(Fore.GREEN+"Username disponible")
                    break
            else:
                print(Fore.RED+"Username no valido, ingresa de nuevo")
                username = questionary.text("Username:").ask().strip()
        # Validando correo no repetido y formato
        email = questionary.text("Correo:").ask().strip()
        listCorreos = [elemento[2] for elemento in response.json()['result']]
        while(True):
            if(re.search(r'@', email)):
                coincidencia = 0
                for correo in listCorreos:
                    if (correo == email):
                        coincidencia = 1
                if (coincidencia == 1):
                    print(Fore.RED+"Correo ya registrado, ingrese otro")
                    email = questionary.text("Correo:").ask().strip()  
                else:
                    break
            else:
                print(Fore.RED+"No cumple el formato de correo, ingresa de nuevo")
                email = questionary.text("Correo:").ask().strip()  
    else:
        print(Fore.RED + "Error servidor, vuelva a intentar")
    # Generar contraseña aleatoria
    caracteres = string.ascii_letters + string.digits + string.punctuation
    passwd = ''.join(random.choice(caracteres) for _ in range(8))
    hash_sha512 = hashlib.sha512()
    hash_sha512.update(passwd.encode("utf-8"))
    # Creando usuario
    respoCrear = requests.post(url = endpointBase+ "/crearUsuario", headers = {"Content-Type": "application/json"}, 
                               data=json.dumps({"username":username, "passwd":hash_sha512.hexdigest(),"email":email,"flagAZ":True,"Roles_idRoles":2}))
    if(respoCrear.status_code == 200):
        print(Fore.GREEN+"Usuario creado exitosamente")
        crearUsuarioEnOpenStack(username, passwd)
        send_email("[OLIMPUS] Credenciales de acceso - PUCP", email, username, passwd)
        print(Fore.GREEN+"Correo enviado con credenciales")
        gestionarUsuarios(usuario, endpointBase)
    else:
        print("Error en el servidor, vuelva a intentar")
        gestionarUsuarios(usuario, endpointBase)


def eliminarUsuario(usuario, endpointBase):
    response = requests.get(url = endpointBase+"/allUsers", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        usuarios = response.json()['result']
        print(Fore.CYAN+"* Lista de Usuarios existentes")
        listaUsuarios = []
        for i in range(0, len(usuarios)):
            if(usuarios[i][1] == usuario.username):
                continue
            else:
                listaUsuarios.append(usuarios[i][1])
        listaUsuarios.append("* Regresar")
        usuarioEliminar = questionary.rawselect("Elija un usuario a eliminar: (O seleccione la última opción para volver)", choices=listaUsuarios).ask()
        if(usuarioEliminar=="* Regresar"):
            gestionarUsuarios(usuario, endpointBase)
        idEliminar = [user[0] for user in usuarios if user[1] == usuarioEliminar] [0]
        resultadoEliminar = requests.get(url = endpointBase+"/eliminarUsuario/"+str(idEliminar), 
                                         headers = {"Content-Type": "application/json"})
        if(resultadoEliminar.status_code==200 and resultadoEliminar.json()["result"] == "Correcto"):
            print(Fore.GREEN+"Usuario Eliminado Correctamente")
        else:
            print(Fore.RED+"Hubo un problema al eliminar, intente nuevamente")
    else:
        print(Fore.RED+"Error en el servidor")
        gestionarUsuarios(usuario, endpointBase)


def listarAllUsers(usuario, endpointBase):
    response = requests.get(url = endpointBase+ "/allUsers", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        usuarios = response.json()['result']
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("idUser", justify="right")
        table.add_column("Username",justify="center")
        table.add_column("Correo", justify="left")
        table.add_column("¿Eligió AZs?", justify="lef")
        table.add_column("Rol", justify="left")
        for user in usuarios:
            table.add_row(str(user[0]), user[1], user[2], "Si" if user[3]==1 else "No", "Usuario" if user[4]==2 else "Operador")
        console.print(table)
        gestionarUsuarios(usuario, endpointBase)
    else:
        print(Fore.RED + "Error en el servidor")
        gestionarUsuarios(usuario, endpointBase)


def crearUsuarioEnOpenStack(username, passwd):
    comando = f"openstack user create --domain default --password {passwd} {username}"
    resourceManager.execRemoto(comando,"10.20.10.221")