from Recursos.funcionGestionTopologias import graficarTopologia

def gener_hijos(parent, numHijos, links, nodos, contador):
    for _ in range(numHijos):
        contador += 1
        hijo = f'sw{contador}'
        nodos.append(hijo)
        enlace = (parent, hijo)
        links.append(enlace)
    return links, nodos, contador

def gener_vms(parent, numHijos, links, nodos, contador_vms):
    for _ in range(numHijos):
        contador_vms += 1
        hijo = f'vm{contador_vms}'
        nodos.append(hijo)
        enlace = (parent, hijo)
        links.append(enlace)
    return links, nodos, contador_vms

def generarArbol(numHijos, nivel):  
    nodoInicial = 'sw1'
    nodos = [nodoInicial]
    links = []
    contador = 1
    contador_vms = 0
    for i in range(1, nivel + 1):
        num_enlaces = numHijos ** i
        nodos_elegir = int(num_enlaces / numHijos)
        if i == 1:
            nodos_elegidos = [nodoInicial]
        else:
            nodos_elegidos = nodos[-nodos_elegir:]
        if(i==nivel):
            for nodo in nodos_elegidos:
                links, nodos, contador_vms = gener_vms(nodo, numHijos, links, nodos, contador_vms)
        else:
            for nodo in nodos_elegidos:
                links, nodos, contador = gener_hijos(nodo, numHijos, links, nodos, contador)
    VMS = numHijos**nivel
    listaSWs = nodos[:-VMS]
    listaVMs = nodos[VMS-1:]
    return (links, listaSWs, listaVMs)