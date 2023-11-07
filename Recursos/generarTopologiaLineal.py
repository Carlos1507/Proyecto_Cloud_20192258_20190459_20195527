import copy

def generarLineal(numNodos):  
    nodos = []
    ## generar nodos
    for i in range(1, numNodos+1):
        nodos.append(f'vm{i}')
    # Conectar los nodos
    nodosAltern = copy.deepcopy(nodos)
    nodosAltern.insert(0, nodosAltern.pop())
    linksSWs = list(zip(nodos, nodosAltern))
    linksSWs.remove((nodos[0],nodos[-1]))
    return (linksSWs, nodos)