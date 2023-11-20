import networkx as nx
import os
import matplotlib.pyplot as plt
import random
import string

def generar_id_aleatorio():
    caracteres = string.ascii_letters + string.digits
    id_aleatorio = ''.join(random.choice(caracteres) for _ in range(8))
    return id_aleatorio


def graficarTopologia(title, listaVMs, listaEnlaces, flagGuardar=False, nameSlice=None):
    G = nx.Graph()

    G.add_nodes_from(listaVMs)
    G.add_edges_from(listaEnlaces)

    fig, ax = plt.subplots(figsize=(9, 6))
    layout = nx.spring_layout(G)

    node_colors = 'lightgreen'
    node_edge_colors = 'black'
    node_size = 800
    
    nx.draw_networkx_nodes(G, layout, ax=ax, node_shape='o', node_color=node_colors, edgecolors=node_edge_colors, node_size=node_size)
    nx.draw_networkx_edges(G, layout, ax=ax)
    edge_labels = {arista: f"Enlace {i+1}" for i, arista in enumerate(G.edges())}

    nx.draw_networkx_edge_labels(G, layout, edge_labels=edge_labels)

    node_labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, layout, labels=node_labels, ax=ax, font_size=10, verticalalignment='center', horizontalalignment='center')

    ax.set_title(title)
    if flagGuardar:
        current_dir = os.getcwd()
        nombreArchivo = "slice"+generar_id_aleatorio()+".png"
        output_path = os.path.join(current_dir,nombreArchivo)
        plt.savefig(output_path, format='png')
        return nombreArchivo
    else:
        plt.show()

def graficarTopologiaImportada(datos):
    fechaCreacion = datos['fecha']
    nombreSlice = datos['nombre']
    nombresVMs = [vm['nombre'] for vm in datos['vms']]
    links = datos['enlaces']
    graficarTopologia("Topología importada: "+nombreSlice+" Creado: "+fechaCreacion, nombresVMs, links, False)
    return {'nombre':datos['nombre'], 'enlaces': datos['enlaces'], 'vms': datos['vms'], 'fecha': datos['fecha']} 