from openstack_sdk import password_authentication_with_scoped_authorization
from openstack_sdk import token_authentication_with_scoped_authorization
from openstack_sdk import create_network
from resourceManager import execRemoto
from openstack_sdk import create_subnet
from openstack_sdk import create_port
from openstack_sdk import create_instance
import json

def crearVM(username, password,project_name, network_name, subnet_name, cidr):
    #Crear nuevo proyecto:
    execRemoto(f"openstack project create {project_name}","10.20.10.221")

    # Asignar al usuario el rol "admin" en el proyecto
    execRemoto(f"openstack role add --project {project_name} --user {username} admin","10.20.10.221")

    # Datos previos
    gatewayIP = '10.20.10.221'
    keystoneEndpoint = 'http://' + gatewayIP + ':5000/v3'
    neutronEndpoint = 'http://' + gatewayIP + ':9696/v2.0'
    novaEndpoint = 'http://' + gatewayIP + ':8774/v2.1'
    adminUserPassword = password
    adminUserUsername = username
    adminUserDomainName = 'Default'
    domainId = 'default'
    adminProjectName = project_name
    ip_version = '4'

    # Generando el token de usuario admin
    resp1 = password_authentication_with_scoped_authorization(keystoneEndpoint, adminUserDomainName, adminUserUsername, adminUserPassword, domainId, adminProjectName)

    # Validando
    if resp1.status_code == 201:
        admin_token = resp1.headers['X-Subject-Token']

        # Generando token para el proyecto
        resp2 = token_authentication_with_scoped_authorization(keystoneEndpoint, admin_token, domainId, project_name)
        if resp2.status_code == 201:
            token_for_project = resp2.headers['X-Subject-Token']

            # Ejecutando Network Creation
            resp3 = create_network(neutronEndpoint, token_for_project, network_name)
            if resp3.status_code == 201:
                network_created = resp3.json()
                network_id = network_created["network"]["id"]

                # Ejecutando Subnetwork Creation
                resp4 = create_subnet(neutronEndpoint, token_for_project, network_id, subnet_name, ip_version, cidr)
                if resp4.status_code == 201:
                    
                    # Ejecutando Ports Creation
                    port_name = "puerto1" #!!!!!!!!!!!!!!!!!!!!
                    project_id = execRemoto("openstack project show " + project_name + " | grep ' id ' | awk '{print $4}'","10.20.10.221")
                    resp5 = create_port(neutronEndpoint, token_for_project, port_name, network_id, project_id)
                    if resp5.status_code == 201:
                        print('PORT CREATED SUCCESSFULLY')
                        port_created = resp5.json()
                        port_id = port_created["port"]["id"]

                        # Ejecutando Instances Creation
                        instance_name = "instance1" #!!!!!!!!!!!!!!!!!!!!
                        instance_flavor_id = '766fa567-86c4-42b4-a3a1-f2316cdb0b7d' #200MBRAM_1VCPUs_1GBRoot
                        instance_image_id = '474e67b0-5022-43e7-9312-51085691a37e' #cirrus
                        instance_networks = [{"port": port_id}]
                        resp1 = create_instance(novaEndpoint, token_for_project, instance_name, instance_flavor_id, instance_image_id, instance_networks)
                        print(resp1.status_code)
                        if resp1.status_code == 202:
                            print('INSTANCE CREATED SUCCESSFULLY')
                            instance_created = resp1.json()
                            print(json.dumps(instance_created))
                        else:
                            print('FAILED INSTANCE CREATION')
                            return
                    else:
                        print('FAILED PORT CREATION')
                        return
                else:
                    print('FAILED SUBNET CREATION')
                    return
            else:
                print('FAILED NETWORK CREATION')
                return
        else:
            print('FAILED AUTHENTICATION FOR PROJECT ' + project_name)
            return
    else:
        print('FAILED ADMIN AUTHENTICATION')
        return

if __name__ == "__main__":
    # Para crear slice, pedir q ingrese contraseña?
    crearVM('angelo123','N4Ak=0GV','prueba','gira','giraSub','10.0.1.0/24')