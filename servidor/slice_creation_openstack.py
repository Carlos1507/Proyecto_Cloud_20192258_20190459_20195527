from openstack_sdk import password_authentication_with_scoped_authorization
from openstack_sdk import token_authentication_with_scoped_authorization
from openstack_sdk import create_network
from resourceManager import execRemoto
from openstack_sdk import create_subnet
from openstack_sdk import create_port
from openstack_sdk import create_instance
import json, os, platform
import re
from collections import Counter
sistema = platform.system()

if(sistema =="Linux"):
    from funcionConsultasBD import ejecutarSQLlocal as ejecutarConsultaSQL
    from resourceManager import execLocal as execCommand
else:
    from funcionConsultasBD import ejecutarSQLRemoto as ejecutarConsultaSQL
    from resourceManager import execRemoto as execCommand

def generarToken(username,password,project_name):
    # Datos previos
    gatewayIP = '10.20.10.221'
    keystoneEndpoint = 'http://' + gatewayIP + ':5000/v3'
    adminUserPassword = password
    adminUserUsername = username
    adminUserDomainName = 'Default'
    domainId = 'default'
    adminProjectName = project_name

    # Generando el token de usuario admin
    resp1 = password_authentication_with_scoped_authorization(keystoneEndpoint, adminUserDomainName, adminUserUsername, adminUserPassword, domainId, adminProjectName)

    # Validando
    if resp1.status_code == 201:
        admin_token = resp1.headers['X-Subject-Token']

        # Generando token para el proyecto
        resp2 = token_authentication_with_scoped_authorization(keystoneEndpoint, admin_token, domainId, project_name)
        if resp2.status_code == 201:
            token_for_project = resp2.headers['X-Subject-Token']
            return token_for_project
        else:
            print('FAILED AUTHENTICATION FOR PROJECT ' + project_name)
            return
    else:
        print('FAILED ADMIN AUTHENTICATION')
        return

def obtenerNombresEnlaces(datos):
    nombres_vm_en_orden = [nombre for enlace in datos["enlaces"] for nombre in enlace]
    numeros_vm = [nombre[2:] for nombre in nombres_vm_en_orden]
    pares_numeros = [numeros_vm[i] + numeros_vm[i + 1] for i in range(0, len(numeros_vm) - 1, 2)]
    nombres_enlaces = ["link" + par for par in pares_numeros]
    return nombres_enlaces

def crearNetwork(token_for_project,network_name,subnet_name,ip_version, cidr):
    # Datos previos
    gatewayIP = '10.20.10.221'
    neutronEndpoint = 'http://' + gatewayIP + ':9696/v2.0'
    # Ejecutando Network Creation
    resp3 = create_network(neutronEndpoint, token_for_project, network_name)
    if resp3.status_code == 201:
        network_created = resp3.json()
        network_id = network_created["network"]["id"]

        # Ejecutando Subnetwork Creation
        resp4 = create_subnet(neutronEndpoint, token_for_project, network_id, subnet_name, ip_version, cidr)
        if resp4.status_code == 201:
            #print('SUBNET CREATED SUCCESSFULLY')
            return network_id
        else:
            print('FAILED SUBNET CREATION')
            return
    else:
        print('FAILED NETWORK CREATION')
        return

def obtenerNombresPuertos(nombresEnlaces):
    resultado = {}
    for nombre in nombresEnlaces:
        numero1 = nombre[4]
        numero2 = nombre[5]
        nuevoElemento1 = f"vm{numero1}_{nombre}"
        nuevoElemento2 = f"vm{numero2}_{nombre}"
        resultado[nombre] = [nuevoElemento1, nuevoElemento2]
    return resultado

def crearPuertos(token_for_project,project_id,port_name,network_id):
    # Datos previos
    gatewayIP = '10.20.10.221'
    neutronEndpoint = 'http://' + gatewayIP + ':9696/v2.0'
    # Ejecutando ports creation
    resp5 = create_port(neutronEndpoint, token_for_project, port_name, network_id, project_id)
    if resp5.status_code == 201:
        #print('PORT CREATED SUCCESSFULLY')
        port_created = resp5.json()
        port_id = port_created["port"]["id"]
        return port_id
    else:
        print('FAILED PORT CREATION')
        return

def crearVM(token_for_project,instance_name,instance_flavor_id,instance_image_id,instance_networks):
    # Datos previos
    gatewayIP = '10.20.10.221'
    novaEndpoint = 'http://' + gatewayIP + ':8774/v2.1'
    # Ejecutando Instances Creation
    resp1 = create_instance(novaEndpoint, token_for_project, instance_name, instance_flavor_id, instance_image_id, instance_networks)
    if resp1.status_code == 202:
        instance_created = resp1.json()
        instance_id = instance_created["server"]["id"]
        return instance_id
    else:
        print('FAILED INSTANCE CREATION')
        return
    
def borrarSlice(project_name):
    proyectId = execCommand("openstack project show --format value --column id "+project_name,"10.20.10.221")
    execCommand("openstack server list --project "+proyectId+" -f value -c ID | xargs -I {} openstack server delete {}","10.20.10.221")
    execCommand("openstack port list --project "+proyectId+" -f value -c ID | xargs -I {} openstack port delete {}","10.20.10.221")
    execCommand("openstack subnet list --project "+proyectId+" -f value -c ID | xargs -I {} openstack subnet delete {}","10.20.10.221")
    execCommand("openstack network list --project "+proyectId+" -f value -c ID | xargs -I {} openstack network delete {}","10.20.10.221")
    execCommand("openstack project delete "+proyectId,"10.20.10.221")

def crearSlice(datos,username,password,project_name):
    ip_version = '4'
    base_cidr = '10.0.'
    cidr_suffix = '/24'
    nombresEnlaces = obtenerNombresEnlaces(datos)
    nombrePuertos = obtenerNombresPuertos(nombresEnlaces)
    nombresVm = [vm["nombre"] for vm in datos["vms"]]

    #Crear nuevo proyecto:
    execCommand(f"openstack project create {project_name}","10.20.10.221")

    # Asignar al usuario el rol "admin" en el proyecto
    execCommand(f"openstack role add --project {project_name} --user {username} admin","10.20.10.221")

    # Generar token para proyecto
    token_for_project = generarToken(username,password,project_name)
    project_id = execCommand("openstack project show " + project_name + " | grep ' id ' | awk '{print $4}'","10.20.10.221")

    # Crear redes
    net_id_list = []
    for i, enlace in enumerate(nombresEnlaces, start=1):
        network_name = enlace  
        cidr = f'{base_cidr}{i}.0{cidr_suffix}'  # Actualiza la parte de la IP
        net_id = crearNetwork(token_for_project, network_name, network_name, ip_version, cidr)
        net_id_list.append({enlace: net_id})
    
    # Crear puertos
    port_id_list = []
    for net_id_dict in net_id_list:
        for link, network_id in net_id_dict.items():  # net_id_dict = {"link21": "net_id1"}
            vm_list = nombrePuertos[link]
            for port_name in vm_list:
                port_id = crearPuertos(token_for_project,project_id,port_name,network_id)
                port_id_list.append({port_name: port_id})

    # Crear instancias
    instance_id_list = []
    for instance_name in nombresVm:
        filtered_dict = {key: value for item in port_id_list for key, value in item.items() if instance_name in key}
        instance_networks = [{"port": value} for key, value in filtered_dict.items() if instance_name in key]
        vm_encontrada = next((vm for vm in datos["vms"] if vm["nombre"] == instance_name), None)
        alias_o_nombre = vm_encontrada["alias"] if vm_encontrada and vm_encontrada["alias"] else instance_name
        id_imagen = vm_encontrada["idOpenstackImagen"]
        id_flavor = vm_encontrada["idOpenstackFlavor"]
        instance_id = crearVM(token_for_project,alias_o_nombre,id_flavor,id_imagen,instance_networks)
        instance_id_list.append({instance_name: instance_id})

    # Generar links de acceso
    instance_link_list = []
    for instance_id_dict in instance_id_list:
        for vm_name, vm_id in instance_id_dict.items():
            link = execCommand("nova get-vnc-console "+vm_id+" novnc | grep novnc | awk '{print $4}'","10.20.10.221")
            instance_link_list.append({vm_name: link})
    for enlace in instance_link_list:
        for key, value in enlace.items():
            enlace[key] = value.replace('controller', '10.20.10.221')
    print(instance_link_list)

def edit_EliminarInstancia(id_Vm_OpenStack,name_project):
    numPorts = execCommand("openstack port list --server "+id_Vm_OpenStack+" -c ID -f value | wc -l","10.20.10.221")
    if (numPorts == "1"):
        # Obtener ID de la red a la que pertenece la VM (solo un puerto, pertenece solo a una red)
        nameNetwork = execCommand("openstack server show --format value -c addresses "+id_Vm_OpenStack+" | awk -F '=' '{print $1}'","10.20.10.221")
        network_string = execCommand("openstack network list --project "+name_project+" -c ID -c Name -f value","10.20.10.221")
        lines = network_string.split('\n')
        name_id_net_dic = {line.split()[1]: line.split()[0] for line in lines if line}
        idNetwork = name_id_net_dic[nameNetwork]
        # Obtener ID del puerto asociado a la VM (sería solo 1)
        ipPortAsociadoVMeliminar = execCommand("openstack port list --server "+id_Vm_OpenStack+" -c ID -f value | awk '{print $1}'","10.20.10.221")
        # Borras VM con ID de la VM
        execCommand("openstack server delete "+id_Vm_OpenStack,"10.20.10.221")
        # Borrar puerto antes asociado a la VM eliminada
        execCommand("openstack port delete "+ipPortAsociadoVMeliminar,"10.20.10.221")

        # Obtener ID del puerto restante mediante ID de red
        idPuertoRestante = execCommand("openstack port list --network "+idNetwork+" -c ID -f value","10.20.10.221")
        if(idPuertoRestante is not None and idPuertoRestante != ""):
            # Ver a que VM esta asociado ese puerto restante, obtener ID VM
            idVMdePuertoRestante = execCommand("openstack port show "+idPuertoRestante+" -c device_id -f value","10.20.10.221")
            # Desasociar el puerto de la VM
            execCommand(f"nova interface-detach {idVMdePuertoRestante} {idPuertoRestante}","10.20.10.221")
            # Eliminar el puerto de la VM con el ID
            execCommand("openstack port delete "+idPuertoRestante,"10.20.10.221")

        # Eliminar subnet de la red
        id_subnet = execCommand("openstack subnet list --network "+idNetwork+" -f value -c ID","10.20.10.221")
        execCommand("openstack subnet delete "+id_subnet,"10.20.10.221")
        # Eliminar la red
        execCommand("openstack network delete "+idNetwork,"10.20.10.221")
    else:
        # Obtener los ID de esos puertos asociados a la VM
        network_string = execCommand("openstack port list --server "+id_Vm_OpenStack+" -c ID -f value","10.20.10.221")
        listaPuertos = network_string.split('\n')
        # Obtener nombres de las redes en contacto con la VM a eliminar
        name_IP_nets = execCommand("openstack server show "+id_Vm_OpenStack+" -c addresses -f value","10.20.10.221")
        name_ip_nets_list = re.findall(r'(\w+)=', name_IP_nets)

        network_string = execCommand("openstack network list --project "+name_project+" -c ID -c Name -f value","10.20.10.221")
        lines = network_string.split('\n')
        name_id_net_dic = {line.split()[1]: line.split()[0] for line in lines if line}
        redesContacto = {clave: name_id_net_dic[clave] for clave in name_ip_nets_list}
        
        # Borras VM con ID de la VM
        execCommand("openstack server delete "+id_Vm_OpenStack,"10.20.10.221")
        # Con el numero de puertos asociados, un bucle for y elimnar puertos
        for portID in listaPuertos:
            execCommand("openstack port delete "+portID,"10.20.10.221")

        # Eliminando redes no servibles
        #redesContacto = {'link21': 'e11f308f-30c1-4318-89f9-2fc412c12985', 'link32': '856b9912-8a8f-4114-8c84-6c5ff81589a0'}
        for clave, valor in redesContacto.items():
            vmContacto = execCommand("openstack port list --network "+valor+" -c ID -c Device -f value | grep -c '^'","10.20.10.221")
            # Cuantas instancias hay por red
            if (vmContacto == '1'):
                puerto = execCommand("openstack port list --network "+valor+" -c ID -c Device --format value","10.20.10.221")
                instancia = execCommand("openstack port show "+puerto+" -c device_id -f value","10.20.10.221")
                numPortsVm = execCommand("openstack port list --server "+instancia+" -c ID -f value | wc -l","10.20.10.221")
                if (numPortsVm != '1'):
                    # Obtener ID del puerto restante mediante ID de red
                    idPuertoRestante = execCommand("openstack port list --network "+valor+" -c ID -f value","10.20.10.221")
                    # Ver a que VM esta asociado ese puerto restante, obtener ID VM
                    idVMdePuertoRestante = execCommand("openstack port show "+idPuertoRestante+" -c device_id -f value","10.20.10.221")
                    # Desasociar el puerto de la VM
                    execCommand(f"nova interface-detach {idVMdePuertoRestante} {idPuertoRestante}","10.20.10.221")
                    # Eliminar el puerto de la VM con el ID
                    execCommand("openstack port delete "+idPuertoRestante,"10.20.10.221")
                    # Eliminar subnet de la red
                    id_subnet = execCommand("openstack subnet list --network "+valor+" -f value -c ID","10.20.10.221")
                    execCommand("openstack subnet delete "+id_subnet,"10.20.10.221")
                    # Eliminar la red
                    execCommand("openstack network delete "+valor,"10.20.10.221")

def encontrar_nombre_mas_repetido(cadena1, cadena2):
    matches_cadena1 = re.findall(r'link\d+', cadena1)
    matches_cadena2 = re.findall(r'link\d+', cadena2)
    todos_los_links = matches_cadena1 + matches_cadena2
    contador = Counter(todos_los_links)
    nombre_mas_repetido = max(contador, key=contador.get)
    return nombre_mas_repetido


if __name__ == "__main__":

    # JSON de una topología lineal
    datos = {
        "vms": [
            {"nombre": "vm1", "alias": "", "ram": 100, "cpu": 1.0, "disk": 1, "imagen": "cirros-0.6.2-x86_64-disk.img", "idOpenstackImagen": "474e67b0-5022-43e7-9312-51085691a37e", "idOpenstackFlavor": "766fa567-86c4-42b4-a3a1-f2316cdb0b7d"},
            {"nombre": "vm2", "alias": "", "ram": 100, "cpu": 1.0, "disk": 1, "imagen": "cirros-0.6.2-x86_64-disk.img", "idOpenstackImagen": "474e67b0-5022-43e7-9312-51085691a37e", "idOpenstackFlavor": "766fa567-86c4-42b4-a3a1-f2316cdb0b7d"},
            {"nombre": "vm3", "alias": "", "ram": 100, "cpu": 1.0, "disk": 1, "imagen": "cirros-0.6.2-x86_64-disk.img", "idOpenstackImagen": "474e67b0-5022-43e7-9312-51085691a37e", "idOpenstackFlavor": "766fa567-86c4-42b4-a3a1-f2316cdb0b7d"}, 
            {"nombre": "vm4", "alias": "", "ram": 100, "cpu": 1.0, "disk": 1, "imagen": "cirros-0.6.2-x86_64-disk.img", "idOpenstackImagen": "474e67b0-5022-43e7-9312-51085691a37e", "idOpenstackFlavor": "766fa567-86c4-42b4-a3a1-f2316cdb0b7d"}
        ],
        "enlaces": [('vm2', 'vm1'), ('vm3', 'vm2'), ('vm4', 'vm3')],
        "nombre": "lineal3",
        "fecha": "18/11/2023",
        'AZ': 'Golden Zone'
    }

    # Datos previos
    username = 'angelo123'
    password = 'ah7Z6JQQ'  #pedir a usuario
    project_name = 'prueba'  #pedir a usuario

    #crearSlice(datos,username,password,project_name)
    #borrarSlice(project_name)


    ## Editar: Eliminar una VM
    #id_Vm_OpenStack = "334eb831-771b-471f-9846-74c232c19000"
    #name_project = "prueba"
    #edit_EliminarInstancia(id_Vm_OpenStack,name_project)


    # Editar: Eliminar un enlace
    id1_vm_openst = "6c7c9381-db5f-4ffd-9ef3-57169250d07e"
    nombre1_NOalias = "vm4"
    id2_vm_openst = "9a554e88-a91f-4b7f-a00a-67f82ab2aa2a" 
    nombre2_NOalias = "vm3"
    name_project = "prueba"
    username = 'angelo123'
    password = 'ah7Z6JQQ'  #pedir a usuario

    # Obtener ID de la red que comparten ambas instancias
    list_id_vm = [id1_vm_openst,id2_vm_openst]
    answer = []
    for id in list_id_vm:
        nameNetworks = execCommand("openstack server show --format value -c addresses "+id+" | awk -F '=' '{print $1}'","10.20.10.221")
        answer.append(nameNetworks)
    commonNet = encontrar_nombre_mas_repetido(answer[0],answer[1])
    network_string = execCommand("openstack network list --project "+name_project+" -c ID -c Name -f value","10.20.10.221")
    lines = network_string.split('\n')
    name_id_net_dic = {line.split()[1]: line.split()[0] for line in lines if line}
    idNetwork = name_id_net_dic[commonNet]
    # Obtener numero de puertos por la network
    numPorts = execCommand("openstack port list --network "+idNetwork+" -c ID -f value | wc -l","10.20.10.221")
    if (numPorts == "2"):
        # Numero de puertos asociado a cada VM que pertenece a esa red en comun
        numPorts_inst1 = execCommand("openstack port list --server "+id1_vm_openst+" -c ID -f value | wc -l","10.20.10.221")
        numPorts_inst2 = execCommand("openstack port list --server "+id2_vm_openst+" -c ID -f value | wc -l","10.20.10.221")
        if (numPorts_inst1 == "1" or numPorts_inst2 == "1"):
            if (numPorts_inst1 != numPorts_inst2):
                if "1" in numPorts_inst1:
                    # Si instance1 tiene 1 port, elimino port de la otra instance
                    id_port_elimnar_inst2 = execCommand("openstack port list --device-id "+id2_vm_openst+" --network "+idNetwork+" -c ID -f value","10.20.10.221")
                    execCommand(f"nova interface-detach {id2_vm_openst} {id_port_elimnar_inst2}","10.20.10.221")
                    execCommand("openstack port delete "+id_port_elimnar_inst2,"10.20.10.221")
                else:
                    # Si instance2 tiene 1 port, elimino port de la otra instance
                    id_port_elimnar_inst1 = execCommand("openstack port list --device-id "+id1_vm_openst+" --network "+idNetwork+" -c ID -f value","10.20.10.221")
                    execCommand(f"nova interface-detach {id1_vm_openst} {id_port_elimnar_inst1}","10.20.10.221")
                    execCommand("openstack port delete "+id_port_elimnar_inst1,"10.20.10.221")
            else:
                # Crear una red, subnet, 1 puerto, asociarlo a una instance 1 (convencion)
                token_for_project = generarToken(username,password,name_project)
                
                project_id = execCommand("openstack project show " + project_name + " | grep ' id ' | awk '{print $4}'","10.20.10.221")
                numero = re.search(r'\d+', nombre1_NOalias)
                numero = numero.group()
                network_name = f"link{numero}X"

                subnets_str = execCommand("openstack subnet list --project "+project_name+" -c Subnet --format value","10.20.10.221")
                subnets = subnets_str.split('\n')
                subnet_mas_alta = max(subnets, key=lambda x: int(x.split(".")[2]))
                octetos = subnet_mas_alta.split(".")
                tercer_digito = int(octetos[2]) + 1
                octetos[2] = str(tercer_digito)
                cidr = ".".join(octetos)
                net_id = crearNetwork(token_for_project, network_name, network_name, '4', cidr)

                port_name = nombre1_NOalias+"_"+network_name
                port_id = crearPuertos(token_for_project,project_id,port_name,net_id)

                # Identificar puerto que sera eliminado:
                id_port_elimnar_inst1 = execCommand("openstack port list --device-id "+id1_vm_openst+" --network "+idNetwork+" -c ID -f value","10.20.10.221")

                # Asociar nuevo puerto a instancia1
                execCommand(f"nova interface-attach --port-id {port_id} {id1_vm_openst}","10.20.10.221")

                # Eliminar puerto
                execCommand(f"nova interface-detach {id1_vm_openst} {id_port_elimnar_inst1}","10.20.10.221")
                execCommand("openstack port delete "+id_port_elimnar_inst1,"10.20.10.221")
                
        else:
            # Lo que queda es desasociar ambos puertos, eliminarlos y luego a la red eliminarla
            id_port_elimnar_inst2 = execCommand("openstack port list --device-id "+id2_vm_openst+" --network "+idNetwork+" -c ID -f value","10.20.10.221")
            execCommand(f"nova interface-detach {id2_vm_openst} {id_port_elimnar_inst2}","10.20.10.221")
            execCommand("openstack port delete "+id_port_elimnar_inst2,"10.20.10.221")
            id_port_elimnar_inst1 = execCommand("openstack port list --device-id "+id1_vm_openst+" --network "+idNetwork+" -c ID -f value","10.20.10.221")
            execCommand(f"nova interface-detach {id1_vm_openst} {id_port_elimnar_inst1}","10.20.10.221")
            execCommand("openstack port delete "+id_port_elimnar_inst1,"10.20.10.221")
            # Eliminar subnet de la red
            id_subnet = execCommand("openstack subnet list --network "+idNetwork+" -f value -c ID","10.20.10.221")
            execCommand("openstack subnet delete "+idNetwork,"10.20.10.221")
            # Eliminar la red
            execCommand("openstack network delete "+idNetwork,"10.20.10.221")