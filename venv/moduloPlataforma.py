import questionary
from colorama import Fore, Style, init

def seleccionarPlataforma():
    opcionPlataforma = questionary.select("Seleccione la plataforma:", choices=["1. Linux", "2. OpenStack", "0. Salir"]).ask()
    if(opcionPlataforma == "1. Linux" or opcionPlataforma=="2. OpenStack"):
        return
    else:
        return