def gener_hijos(parent, numHijos, links, nodos, contador):
    for _ in range(numHijos):
        contador += 1
        hijo = f'vm{contador}'
        nodos.append(hijo)
        enlace = (parent, hijo)
        links.append(enlace)
    return links, nodos, contador

def gener_vms(parent, numHijos, links, nodos, contador):
    for _ in range(numHijos):
        contador += 1
        hijo = f'vm{contador}'
        nodos.append(hijo)
        enlace = (parent, hijo)
        links.append(enlace)
    return links, nodos, contador

def generarArbol(numHijos, nivel):  
    nodoInicial = 'vm1'
    nodos = [nodoInicial]
    links = []
    contador = 1
    for i in range(1, nivel + 1):
        num_enlaces = numHijos ** i
        nodos_elegir = int(num_enlaces / numHijos)
        if i == 1:
            nodos_elegidos = [nodoInicial]
        else:
            nodos_elegidos = nodos[-nodos_elegir:]
        if(i==nivel):
            for nodo in nodos_elegidos:
                links, nodos, contador = gener_vms(nodo, numHijos, links, nodos, contador)
        else:
            for nodo in nodos_elegidos:
                links, nodos, contador = gener_hijos(nodo, numHijos, links, nodos, contador)
    return (links, nodos)