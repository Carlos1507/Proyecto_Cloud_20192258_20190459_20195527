import subprocess
import paramiko
import random
def generar_direccion_mac():
    direccion_mac = [random.choice('0123456789abcdef') for _ in range(12)]
    direccion_mac_str = ':'.join(direccion_mac)
    z=direccion_mac_str.split(":")
    direccion_mac_str=str(z[0])+str(z[1])+":"+str(z[2])+str(z[3])+":"+str(z[4])+str(z[5])+":"+str(z[6])+str(z[7])+":"+str(z[8])+str(z[9])+":"+str(z[10])+str(z[11])
    return direccion_mac_str
def ejecLocal(comando):
    resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)   

def funcion_script_C(nombreovs,idvlan1,red1,dhcp1range):
    comando="sudo ovs-vsctl add-port "+ nombreovs +" vlan"+ str(idvlan1)+" tag="+str(idvlan1)
    ejecLocal(comando)
    comando="sudo ovs-vsctl set interface vlan"+str(idvlan1)+" type=internal"
    ejecLocal(comando)
    comando="sudo ip link set dev vlan"+str(idvlan1)+" up"
    ejecLocal(comando)

    nombreGWVlan1 = "vlan"+idvlan1    
    
    iname1 = "ns-vlan"+idvlan1
    
    comando="sudo ovs-vsctl add-port "+nombreovs+" "+iname1+" tag="+idvlan1
    ejecLocal(comando)
    comando="sudo ovs-vsctl set interface "+iname1+" type=internal"
    ejecLocal(comando)
    comando="sudo ip link set dev "+iname1+" up"
    ejecLocal(comando)
    
    ###
    a=red1.split(".")
    mask=red1.split("/")
    ipGW1=a[0]+"."+a[1]+"."+a[2]+".1/"+str(mask[1]) 
    comando="sudo ip add add "+ipGW1+" dev vlan"+idvlan1
    ejecLocal(comando)
    ####
    nsDhcp1= "ns-dhcp-vlan"+idvlan1
    comando="sudo ip netns add "+nsDhcp1
    ejecLocal(comando)
    comando="sudo ip netns exec "+nsDhcp1+" ip link set dev lo up"
    ejecLocal(comando)
    comando="sudo ip link set "+iname1+" netns "+nsDhcp1
    ejecLocal(comando)
    comando="sudo ip netns exec "+nsDhcp1+" ip link set dev "+iname1+" up"
    ejecLocal(comando)

    a=red1.split(".")
    mask=red1.split("/")
    ipDHCP1=a[0]+"."+a[1]+"."+a[2]+".2/"+str(mask[1]) 

    comando="sudo ip netns exec "+nsDhcp1+" ip add add "+ ipDHCP1+" dev "+iname1
    ejecLocal(comando)
    comando="sudo ip netns exec "+nsDhcp1+" dnsmasq --interface="+iname1+" --dhcp-range="+dhcp1range+" --dhcp-option=6,8.8.8.8 --dhcp-option=3,"+ipGW1.split("/")[0]
    ejecLocal(comando)
    return nombreGWVlan1

def funcion_scriptD(nombreVM,nombreOVS,vlanID,comandoVM):
    username = "ubuntu"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("10.0.0.50","22",username)
    nombreVMf = str(nombreVM)+"y"+str(vlanID)
    comando="sudo ip tuntap add mode tap name "+nombreVMf
    client.exec_command(comando)
    comando = "sudo ovs-vsctl add-port "+ nombreOVS +" "+ nombreVMf+" tag="+vlanID
    client.exec_command(comando)
    comando="sudo ip link set dev "+nombreVMf+" up"
    client.exec_command(comando)
    comando=comandoVM
    client.exec_command(comando)
    comando="sudo ip link set dev "+nombreVMf+" up"
    client.exec_command(comando)
    client.close()
def crear_enlaces(parte1,parte2,vlanid):
    username = "ubuntu"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("10.0.0.50","22",username)
    w1 = parte1.replace("vm", "")
    w2 = parte2.replace("vm", "")
    ovs_enlace = "vm"+str(w1)+str(w2)+"y"+str(vlanid)
    tap1 = ovs_enlace+"p"+w1
    tap2 = ovs_enlace+"p"+w2
    comando="sudo ovs-vsctl add-br "+ ovs_enlace
    client.exec_command(comando)
    comando="sudo ip link set dev "+ ovs_enlace+" up"
    client.exec_command(comando)
    comando="sudo ip tuntap add mode tap name "+tap1
    client.exec_command(comando)
    comando="sudo ip tuntap add mode tap name "+tap2
    client.exec_command(comando)
    comando = "sudo ovs-vsctl add-port "+ ovs_enlace +" "+ tap1
    client.exec_command(comando)
    comando = "sudo ovs-vsctl add-port "+ ovs_enlace +" "+ tap2
    client.exec_command(comando)
    comando="sudo ip link set dev "+tap1+" up"
    client.exec_command(comando)
    comando="sudo ip link set dev "+tap2+" up"
    client.exec_command(comando)
    return [ovs_enlace,tap1,tap2]

def internet_vlan(vlanid,ipred):
    regla1="sudo iptables -A FORWARD -i ens3 -d "+ipred+" -j ACCEPT"
    regla2="sudo iptables -A FORWARD -o ens3 -s "+ipred+" -j ACCEPT"
    ejecLocal(regla1)
    ejecLocal(regla2)
def crear_slice(datos):
    lista_para_red = list(range(10, 251))
    elemento_aleatorio = random.choice(lista_para_red)
    red="10.10."+str(elemento_aleatorio)+".0/24"
    vlanid=str(elemento_aleatorio)
    rangodhcp="10.10."+str(elemento_aleatorio)+".3,10.10."+str(elemento_aleatorio)+".254"
    gatewayvlan =funcion_script_C("br-vlan",vlanid,red,rangodhcp)

    lista_vms = []
    for vm in datos['vms']:
        vm_info = {
            'nombre': vm['nombre'],
            'ram': vm['ram'],
            'cpu': vm['cpu'],
            'disk': vm['disk'],
            'imagen': vm['imagen']
        }
        lista_vms.append(vm_info)

    lista_enlaces = list(datos['enlaces'])

    nombres_enlace =[]
    for i in lista_enlaces:
        nombres_enlace.append(crear_enlaces(i[0],i[1],vlanid))

    lista_vms_para_meterenfuncion=[]
    for i in lista_vms:
        lista_interfaces=[]
        for x in nombres_enlace:
            if i["nombre"] == str(str(x[1][:2])+str(x[1][-1])):
                lista_interfaces.append(x[1])
            if i["nombre"] == str(str(x[2][:2])+str(x[2][-1])):
                lista_interfaces.append(x[2])
        lista_vms_para_meterenfuncion.append([i,lista_interfaces])

    lf = []
    for i in lista_vms_para_meterenfuncion:
        puertoVNC= random.choice(list(range(1, 100)))
        ram = str(i[0]["ram"])
        cpus = str(int(i[0]["cpu"]))
        mac=generar_direccion_mac()
        nombreVMf=str(i[0]["nombre"]+"y"+str(vlanid))
        comando_vm = "sudo qemu-system-x86_64 -enable-kvm -cpu host -m "+ram+" -smp "+cpus+" -vnc 0.0.0.0:"+str(puertoVNC)+" -netdev tap,id="+nombreVMf+",ifname="+nombreVMf+",script=no,downscript=no -device e1000,netdev="+nombreVMf  
        for x in i[1]:
            comando_vm =comando_vm+" -netdev tap,id="+x+",ifname="+x+",script=no,downscript=no -device e1000,netdev="+x
        trfinal =",mac="+mac+" -daemonize -snapshot "+i[0]["imagen"]
        comando_vm =comando_vm+str(trfinal)
        funcion_scriptD(i[0]["nombre"],"br-linuxw3",vlanid,comando_vm)
        lf.append([i[0]["nombre"],str(puertoVNC+5900)])
    return [vlanid,lf]