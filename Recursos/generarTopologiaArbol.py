from Recursos.funcionGestionTopologias import graficarTopologia
links = []
global nodos
nodos = []
global numHijos
nodoInicial = 'sw1'
nodos = [nodoInicial]
links = []
contador = 1
contador_vms = 0

def gener_hijos(parent, numHijos):
    global nodos, contador
    for _ in range(numHijos):
        contador += 1
        hijo = f'sw{contador}'
        nodos.append(hijo)
        enlace = (parent, hijo)
        links.append(enlace)

def gener_vms(parent, numHijos):
    global nodos, contador_vms
    for _ in range(numHijos):
        contador_vms += 1
        hijo = f'vm{contador_vms}'
        nodos.append(hijo)
        enlace = (parent, hijo)
        links.append(enlace)

def generarArbol(numHijos, nivel):  
    for i in range(1, nivel + 1):
        num_enlaces = numHijos ** i
        nodos_elegir = int(num_enlaces / numHijos)
        if i == 1:
            nodos_elegidos = [nodos[-1]]
        else:
            nodos_elegidos = nodos[-nodos_elegir:]
        if(i==nivel):
            for nodo in nodos_elegidos:
                gener_vms(nodo, numHijos)
        else:
            for nodo in nodos_elegidos:
                gener_hijos(nodo, numHijos)
    VMS = numHijos**nivel
    listaSWs = nodos[:-VMS]
    listaVMs = nodos[VMS-1:]
    return (links, listaSWs, listaVMs)