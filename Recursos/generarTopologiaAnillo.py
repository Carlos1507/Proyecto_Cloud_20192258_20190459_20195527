import copy

def generarAnillo(numNodos):  
    nodos = []
    ## generar nodos
    for i in range(1, numNodos+1):
        nodos.append(f'vm{i}')
    # Conectar los nodos
    nodosAltern = copy.deepcopy(nodos)
    nodosAltern.insert(0, nodosAltern.pop())
    links = list(zip(nodos, nodosAltern)) 
    # Resultado
    return (links, nodos)