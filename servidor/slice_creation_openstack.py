from openstack_sdk import password_authentication_with_scoped_authorization
from openstack_sdk import token_authentication_with_scoped_authorization
from openstack_sdk import create_network
from resourceManager import execRemoto
from openstack_sdk import create_subnet
from openstack_sdk import create_port
from openstack_sdk import create_instance
import json

def crearProyecto(username,password,project_name):
    #Crear nuevo proyecto:
    execRemoto(f"openstack project create {project_name}","10.20.10.221")

    # Asignar al usuario el rol "admin" en el proyecto
    execRemoto(f"openstack role add --project {project_name} --user {username} admin","10.20.10.221")

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
    print(resp1.status_code)
    if resp1.status_code == 202:
        print('INSTANCE CREATED SUCCESSFULLY')
        instance_created = resp1.json()
        instance_id = instance_created["server"]["id"]
        return instance_id
    else:
        print('FAILED INSTANCE CREATION')
        return

if __name__ == "__main__":

    # JSON de una topología lineal
    datos = {
        "vms": [
            {"nombre": "vm1", "capacidad": "1024", "cpu": "2", "imagen": "cirros.img"},
            {"nombre": "vm2", "capacidad": "1024", "cpu": "2", "imagen": "cirros.img"},
            {"nombre": "vm3", "capacidad": "1024", "cpu": "2", "imagen": "cirros.img"},
            {"nombre": "vm4", "capacidad": "1024", "cpu": "2", "imagen": "cirros.img"}
        ],
        "enlaces": [["vm2", "vm1"], ["vm3", "vm2"], ["vm4", "vm3"]],
        "nombre": "linea1",
        "fecha": "08/11/2023"
    }

    # Datos previos
    username = 'angelo123'
    password = 'N4Ak=0GV'
    project_name = 'prueba'
    ip_version = '4'
    numEnlaces = len(datos["enlaces"])
    base_cidr = '10.0.'
    cidr_suffix = '/24'
    nombresEnlaces = obtenerNombresEnlaces(datos)
    nombrePuertos = obtenerNombresPuertos(nombresEnlaces)
    nombresVm = [vm["nombre"] for vm in datos["vms"]]

    # Crear proyecto
    token_for_project = crearProyecto(username,password,project_name)
    project_id = execRemoto("openstack project show " + project_name + " | grep ' id ' | awk '{print $4}'","10.20.10.221")

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
    instance_flavor_id = '766fa567-86c4-42b4-a3a1-f2316cdb0b7d' #200MBRAM_1VCPUs_1GBRoot
    instance_image_id = '474e67b0-5022-43e7-9312-51085691a37e' #cirros
    for instance_name in nombresVm:
        filtered_dict = {key: value for item in port_id_list for key, value in item.items() if instance_name in key}
        instance_networks = [{"port": value} for key, value in filtered_dict.items() if instance_name in key]
        instance_id = crearVM(token_for_project,instance_name,instance_flavor_id,instance_image_id,instance_networks)
        instance_id_list.append({instance_name: instance_id})
    print(instance_id_list)
    

    # Para crear slice, pedir q ingrese contraseña?
    #crearVM('angelo123','N4Ak=0GV','prueba','gira','giraSub','10.0.1.0/24')