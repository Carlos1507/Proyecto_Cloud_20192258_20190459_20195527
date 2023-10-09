import requests
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init
from Recursos.funcionEnviarMail import send_email
import questionary

console = Console()

def gestionarUsuarios(usuario, endpointBase):
    opcionesSubMenuUsuarios = ["1. Crear Usuario", "2. Visualizar Usuarios", "3. Eliminar Usuario","4. Regresar"]
    opcion = questionary.select("Submenú Gestión de Usuarios: ", choices=opcionesSubMenuUsuarios).ask()
    if(opcion =="4. Regresar"):
        return
    else:
        if(opcion == "1. Crear Usuario"):
            crearUsuario(endpointBase)
        elif(opcion == "2. Visualizar Usuarios"):
            listarAllUsers(usuario, endpointBase)
        elif(opcion == "3. Eliminar Usuario"):
            eliminarUsuario(usuario, endpointBase)
    
def crearUsuario(endpointBase):
    pass

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