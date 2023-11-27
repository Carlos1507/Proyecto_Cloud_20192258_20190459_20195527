import subprocess
import paramiko
import random
def ejecLocal(comando):
    resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)   

def funcion_borrar_local(vlanid):
    comando="sudo ovs-vsctl del-port br-vlan vlan"+str(vlanid)
    try:
        ejecLocal(comando)
    except Exception as e:
        pass
    comando="sudo ovs-vsctl del-port br-vlan ns-vlan"+str(vlanid)
    try:
        ejecLocal(comando)
    except Exception as e:
        pass
    comando="sudo ip netns delete ns-dhcp-vlan"+str(vlanid)
    try:
        ejecLocal(comando)
    except Exception as e:
        pass

    

def borrar_ssh(vlanid):
    username = "ubuntu"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("10.0.0.50","22",username)
    
    comando="ps aux | grep qemu | grep root | awk '{print $2}'"
    stdin,stdout, stderr=client.exec_command(comando)
    salida = stdout.read().decode("utf-8")
    lista=salida.split("\n")
    lista = lista[:-1]
    for i in lista:
        comando="sudo kill "+str(i)
        try:
            client.exec_command(comando)
        except Exception as e:
            pass
        
    comando="sudo ovs-vsctl list-ports br-linuxw3 | grep y"+str(vlanid)
    stdin,stdout, stderr=client.exec_command(comando)
    salida = stdout.read().decode("utf-8")
    lista=salida.split("\n")
    lista = lista[:-1]
    for i in lista:
        comando = "sudo ovs-vsctl del-port br-linuxw3 "+ i
        try:
            client.exec_command(comando)
        except Exception as e:
            pass

    comando="sudo ovs-vsctl show | grep y"+str(vlanid)+" | grep Bridge | awk '{print $2}'"
    stdin,stdout, stderr=client.exec_command(comando)
    salida = stdout.read().decode("utf-8")
    lista=salida.split("\n")
    lista = lista[:-1]
    for i in lista:
        comando = "sudo ovs-vsctl del-br "+ i
        try:
            client.exec_command(comando)
        except Exception as e:
            pass

    comando="sudo ovs-vsctl show | grep y"+str(vlanid)+" | grep Port | awk '{print $2}'"
    stdin,stdout, stderr=client.exec_command(comando)
    salida = stdout.read().decode("utf-8")
    lista=salida.split("\n")
    lista = lista[:-1]
    for i in lista:
        comando = "sudo ip link delete "+ i
        try:
            client.exec_command(comando)
        except Exception as e:
            pass   
    
    comando="sudo ip link | grep y"+str(vlanid)+" | awk '{print $2}'"
    stdin,stdout, stderr=client.exec_command(comando)
    salida = stdout.read().decode("utf-8")
    lista=salida.split("\n")
    lista = lista[:-1]
    lista = [elemento[:-1] for elemento in lista]
    for i in lista:
        comando = "sudo ip link delete "+ i
        try:
            client.exec_command(comando)
        except Exception as e:
            pass   
   
    client.close()
def borrar_slice(vlanid):
    funcion_borrar_local(vlanid)
    borrar_ssh(vlanid)