import networkx as nx
from typing import TypeAlias, Optional
import osmnx as ox
import pickle
import matplotlib.pyplot as plt
import os
from dataclasses import dataclass
from busesactual import *
CityGraph : TypeAlias = nx.Graph
OsmnxGraph : TypeAlias = nx.MultiDiGraph

@dataclass
class Path:
    nodes: list[Cruilla]
    linies: list[Carrer]        

    
def get_osmnx_graph() -> OsmnxGraph:
    filename = 'graf_barcelona'
    if os.path.exists(filename):
        return load_osmnx_graph(filename)
    else:
        ciutat = "Barcelona, Spain"
        graf = ox.graph_from_place(ciutat, network_type='walk', simplify=True)
        multi_graf = nx.MultiDiGraph(graf)
        save_osmnx_graph(graf,"graf_barcelona")
        return multi_graf

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    # guarda el graf g al fitxer filename
    # Obtenir el directori actual
    current_dir = os.getcwd()

    # Definir la ruta del fitxer de sortida
    output_folder = os.path.join(current_dir, filename)
    with open(output_folder, 'wb') as file:
        pickle.dump(g, file)

    
def load_osmnx_graph(filename: str) -> OsmnxGraph: 
    # retorna el graf guardat al fitxer filename
      # Obtenir el directori actual
    current_dir = os.getcwd()

    # Definir la ruta del fitxer
    ruta_document = os.path.join(current_dir, filename)

    # Comprovar si el fitxer existeix
    if not os.path.exists(ruta_document):
        raise FileNotFoundError(f"El fitxer '{filename}' no existeix en el directori actual.")

    # Llegir el graf des del fitxer
    with open(ruta_document, 'rb') as file:
        graf = pickle.load(file)
    return graf
def distance(pos1:tuple[float,float], pos2:tuple[float,float]) -> float:
    d = (pos1[0] - pos2[0])**2 + \
            (pos1[1] - pos2[1])**2
    return d**(1/2)


def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
    # retorna un graf fusió de g1 i g2
    
    city_graph = nx.Graph()
    for node_id, data in g1.nodes(data=True):
        city_graph.add_node(node_id, pos = (data['y'],data['x']), tipus = "Cruilla")
    
    for u, v, data in g1.edges(data=True):
        if u != v:      
            city_graph.add_edge(u,v, longitud= data['length'], tipus = "Carrer")
    
    llista_pos_lat: list[tuple[float]] = []
    llista_pos_lon: list[tuple[float]] = []
    
    for node_id, data in g2.nodes(data = True):
        city_graph.add_node(node_id, pos = data['pos'])
        llista_pos_lat.append(data['pos'][0])
        llista_pos_lon.append(data['pos'][1])
        
    
    cruilles_properes = ox.distance.nearest_nodes(g1, llista_pos_lat,llista_pos_lon, return_dist = False)
    for i, id in enumerate(g2.nodes):
        cruilla_propera_corresponent = cruilles_properes[i]
        if id != cruilla_propera_corresponent:
            city_graph.add_edge(id,cruilla_propera_corresponent,tipus = "Carrer")        
    
    
    for u, v, data in g1.edges(data = True):        
        city_graph.add_edge(u,v, info = 'Bus')
        #falta calcular longitud
        
        
    return city_graph

"""
def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: 
    src_node = ox.distance.nearest_nodes(ox_g, src[0], src[1])
    dst_node = ox.distance.nearest_nodes(ox_g, dst[0], dst[1])

    shortest_path = nx.shortest_path(g, src_node, dst_node)
    shortest_edges = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]
    
    return Path(shortest_path, shortest_edges)
"""
def show(g: CityGraph) -> None:
    # mostra g de forma interactiva en una finestra
    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw_networkx(g, pos=posicions, node_size=10, with_labels=False)
    plt.show()
    
#def plot(g: CityGraph, filename: str) -> None:
   # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename
    ...
#def plot_path(g: CityGraph, p: Path, filename: str) -> None: 
    # mostra el camí p en l'arxiu filename
    ...
def main() -> None:
    
    
    g1 = get_osmnx_graph()
    g2 = get_buses_graph()
    city = build_city_graph(g1, g2)
    """
    g1 = get_osmnx_graph()
    g2 = get_buses_graph()
    city = build_city_graph(g1, g2)
    
    """
    show(city)
    
if __name__ ==  '__main__':
    main()
