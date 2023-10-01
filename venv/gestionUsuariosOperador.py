import requests
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init

console = Console()

def gestionarUsuarios(usuario):
    response = requests.get(url = "http://127.0.0.1:8000/allUsers", 
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
    else:
        print(Fore.RED + "Error en el servidor")