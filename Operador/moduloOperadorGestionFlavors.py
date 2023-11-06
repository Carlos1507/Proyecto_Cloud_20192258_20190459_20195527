import requests, questionary
import Recursos.funcionEjecutarComandoRemoto as ejecutarComando
def gestorFlavors(endpointBase):
    response = requests.get(url = endpointBase+"/allImagenes", 
                                headers = {"Content-Type": "application/json"})
    if(response.status_code == 200):
        imagenes = response.json()['result']
        imagenesOpciones = [imagen[1] for imagen in imagenes]
        imagenNombre = questionary.select("Elija una imagen para crear el flavor: ", choices=imagenesOpciones).ask()
        
        flavorNombre = questionary.text("Indique un nombre para este flavor: ").ask()
        print(imagenNombre)
        print(flavorNombre)
        comando = f"glance image-create --name {flavorNombre} --file imagenes/{imagenNombre} "+ \
                   "--disk-format qcow2 --container-format bare --visibility=public"
        
        ejecutarComando.execRemoto(comando, "10.20.10.221")