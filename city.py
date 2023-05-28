import networkx as nx
from typing import TypeAlias
import osmnx as ox
from buses import *
import pickle
import matplotlib.pyplot as plt

CityGraph : TypeAlias = nx.Graph
OsmnxGraph : TypeAlias = nx.MultiDiGraph
Coord : TypeAlias = tuple[float, float]   # (latitude, longitude)
def get_osmnx_graph() -> OsmnxGraph:
    ciutat = "Barcelona, Spain"
    graf = ox.graph_from_place(ciutat, network_type="all")
    multi_graf = nx.MultiDiGraph(graf)
    return multi_graf

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    # guarda el graf g al fitxer filename
    output_folder = "Desktop/PRACTICA2/" + filename
    with open(output_folder, 'wb') as file:
        pickle.dump(g, file)

    
def load_osmnx_graph(filename: str) -> OsmnxGraph: 
    # retorna el graf guardat al fitxer filename
    ruta_document = 'Desktop/PRACTICA2/' + filename
    with open(ruta_document, 'rb') as file:
        graf = pickle.load(file)
    return graf

def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
     # retorna un graf fusió de g1 i g2
    city_graph = nx.Graph()
    for u, nbrsdict in g1.adjacency():      
        city_graph.add_node(u, info = 'Cruilla')
        # for each adjacent node v and its (u, v) edges' information ...
        for v, edgesdict in nbrsdict.items():
            city_graph.add_node(v, info = 'Cruilla')
            eattr = edgesdict[0]  
            city_graph.add_edge(u,v, **eattr,info = 'Carrer')
            # osmnx graphs are multigraphs, but we will just consider their first edge
             # eattr contains the attributes of the first edge
            # we remove geometry information from eattr because we don't need it and takes a lot of space        
    for node_attrs in g2.nodes.values():
        parada = Parada(node_attrs['parada'].id,node_attrs['parada'].pos)
        city_graph.add_node(parada.id,parada, info = Bus)
    for edge_attrs in g2.edges.values():        
        linia = edge_attrs['linia']  
        city_graph.add_edge(linia.node_origen.pos, linia.node_desti.pos,info = 'Bus')
    
    for node_attrs in g2.nodes.values():
        parada = Parada(node_attrs['parada'].id,node_attrs['parada'].pos)
        cruilla_propera = ox.get_nearest_node(g1, parada.pos)
        city_graph.add_edge(parada, cruilla_propera, info =' Carrer')
        
    return city_graph
    
    
    
   

def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: ...


def show(g: CityGraph) -> None:
    # mostra g de forma interactiva en una finestra
    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos=posicions, with_labels=False,font_size=5,node_size= 5)
    plt.show()

    #nx.draw(g)
    
def plot(g: CityGraph, filename: str) -> None: ...
   # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename

def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename
    
def main() -> None:
    save_osmnx_graph(get_osmnx_graph(), 'graf_barcelona')
    g1 = load_osmnx_graph('graf_barcelona')
    g2 = get_buses_graph()
    city = build_city_graph(g1, g2)
    
    show(city)
if __name__ == '__main__':
    main()
