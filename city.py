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
    
    
    
    city = nx.Graph()
    g1_s = nx.Graph(g1)
    city : CityGraph = nx.compose(g1_s, g2)
    
    return city

#def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: ...


def show(g: CityGraph) -> None:
    # mostra g de forma interactiva en una finestra
    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos=posicions, with_labels=False,font_size=5,node_size= 5)
    plt.show()

    #nx.draw(g)
    
def plot(g: CityGraph, filename: str) -> None: ...
   # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename
#def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename
    
def main() -> None:
    save_osmnx_graph(get_osmnx_graph(), 'graf_barcelona')
    g1 = load_osmnx_graph('graf_barcelona')
    g2 = get_buses_graph()
    city = build_city_graph(g1, g2)
    
    show(city)
if __name__ == '__main__':
    main()
