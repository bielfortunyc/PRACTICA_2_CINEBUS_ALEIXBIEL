import networkx as nx
from typing import TypeAlias, Optional
import osmnx as ox
import pickle
import matplotlib.pyplot as plt
import os
from dataclasses import dataclass
from provabuses import *
CityGraph : TypeAlias = nx.Graph
OsmnxGraph : TypeAlias = nx.MultiDiGraph

@dataclass
class Cruilla:
    id: int
    pos: Coord
    def __init__(self, id: int, pos:Coord) -> None:
        self.id = id
        self.pos = pos
class Carrer:
    node_origen_id: int
    node_desti_id: int
    longitud: float
    info: str
    def __init__(self, node_origen_id: int, node_desti_id: int, longitud: float, info:str) -> None:
        self.node_origen_id = node_origen_id
        self.node_desti_id = node_desti_id
        self.longitud = longitud
        self.info = info

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

def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
    # retorna un graf fusió de g1 i g2
    
    city_graph = nx.Graph()
    for node_id, data in g1.nodes(data=True):
        cruilla = Cruilla(id=node_id, pos=(data['y'],data['x']))
        city_graph.add_node(cruilla.id, pos= cruilla.pos, node = cruilla)
    
    for u, v, data in g1.edges(data=True):
        carrer = Carrer(node_origen_id = u, node_desti_id = v, longitud= data['length'], info = 'Carrer')
        if 'geometry' in data:
            del(data['geometry'])
        city_graph.add_edge(carrer.node_origen_id,carrer.node_desti_id, aresta = carrer)
    
    for node_attrs in g2.nodes.values():
        parada = Parada(id = node_attrs['node'].id, pos = node_attrs['node'].pos)
        city_graph.add_node(parada.id, pos = parada.pos, node = parada, info = 'Bus')
        cruilla_propera = ox.nearest_nodes(g1, parada.pos[0], parada.pos[1])
        city_graph.add_edge(parada.id,cruilla_propera, aresta = cruilla_propera, info = 'Carrer')
        #no detecta que parada i cruilla_propera estiguin ja al graf i genera problems 
        #perquè els torna a afegir sense atributs.
    
    
    for edge_attrs in g2.edges.values():        
        linia = edge_attrs['aresta']  
        city_graph.add_edge(linia.node_origen.id, linia.node_desti.id, info = 'Bus')
    
        
        
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
    positions = {}
    for node_id, data in g.nodes(data=True):
        if 'node' in data:
            positions[node_id] = data['node'].pos
    nx.draw_networkx(g, pos=positions, node_size=10, with_labels=False)
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
