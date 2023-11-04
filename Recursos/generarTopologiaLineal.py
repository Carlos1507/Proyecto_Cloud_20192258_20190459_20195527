from Recursos.funcionGestionTopologias import graficarTopologia
import copy

def generarLineal(numNodos):  
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
    switchesAltern = copy.deepcopy(switches)
    switchesAltern.insert(0, switchesAltern.pop())
    linksSWs = list(zip(switches, switchesAltern))
    linksSWs.remove((switches[0],switches[-1]))
    # Resultado
    return (links+linksSWs, switches, vms)