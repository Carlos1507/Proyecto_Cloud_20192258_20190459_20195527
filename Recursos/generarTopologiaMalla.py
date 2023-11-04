from Recursos.funcionGestionTopologias import graficarTopologia

def generarMalla(numNodos):  
    switches = []
    vms = []
    links = []
    ## generar switches
    for i in range(1, numNodos+1):
        switches.append(f'sw{i}')
    ## generar vms
    for i in range(1, numNodos+1):
        vms.append(f'vm{i}')
    links = list(zip(switches, vms))
    # Conectar los switches
    for i in switches:
        a = switches.index(i)
        lista = switches[a+1:]
        if len(lista)!=0:
            for x in lista:
                links.append((i,x))
    # Resultado
    return (links, switches, vms)