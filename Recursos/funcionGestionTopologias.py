import networkx as nx
import matplotlib.pyplot as plt

def graficarTopologia(title, listaVMs, listaSWs, listaEnlaces):
    G = nx.Graph()

    G.add_nodes_from(listaVMs)
    G.add_nodes_from(listaSWs)
    G.add_edges_from(listaEnlaces)

    fig, ax = plt.subplots(figsize=(8, 5))
    layout = nx.spring_layout(G)

    node_colors = ['yellow' if node in listaSWs else 'white' for node in G.nodes()]
    node_edge_colors = 'black'
    node_size = 800

    nx.draw_networkx_nodes(G, layout, ax=ax, node_shape='o', node_color=node_colors, edgecolors=node_edge_colors, node_size=node_size)
    nx.draw_networkx_edges(G, layout, ax=ax)

    node_labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, layout, labels=node_labels, ax=ax, font_size=10, verticalalignment='center', horizontalalignment='center')

    ax.set_title(title)
    plt.show()