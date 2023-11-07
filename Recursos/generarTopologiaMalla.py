
def generarMalla(numNodos):  
    nodos = []
    links = []
    ## generar nodos
    for i in range(1, numNodos+1):
        nodos.append(f'vm{i}')
    # Conectar los nodos
    for i in nodos:
        a = nodos.index(i)
        lista = nodos[a+1:]
        if len(lista)!=0:
            for x in lista:
                links.append((i,x))
    # Resultado
    return (links, nodos)