import requests, questionary
import Recursos.funcionEjecutarComandoRemoto as ejecutarComando
def gestorImagenesGlance(endpointBase, nombre, filename):
    comando = f"glance image-create --name {nombre} --file /home/ubuntu/imagenes/{filename} "+ \
               "--disk-format qcow2 --container-format bare --visibility=public"
    ejecutarComando.execRemoto(comando, "10.20.10.221")