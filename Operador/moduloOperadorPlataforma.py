import questionary, requests
from colorama import Fore, Style, init

def seleccionarPlataforma(endpointBase):
    opcionPlataforma = questionary.select("Seleccione la plataforma:", choices=["1. Linux", "2. OpenStack", "0. Salir"]).ask()
    if(opcionPlataforma == "1. Linux" or opcionPlataforma=="2. OpenStack"):
        plataformaEnviar = "Linux" if opcionPlataforma == "1. Linux" else "OpenStack"
        response = requests.get(url = endpointBase+"/guardarPlataforma/"+plataformaEnviar, 
                                    headers = {"Content-Type": "application/json"})
        if(response.status_code == 200):
            resultado = response.json()['result']
            if(resultado=="Guardado exitoso"):
                print(Fore.GREEN+"Actualización exitosa")
    else:
        return