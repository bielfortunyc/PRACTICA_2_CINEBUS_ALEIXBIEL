import networkx
from typing import TypeAlias
import osmnx as ox

CityGraph : TypeAlias = networkx.Graph
OsmnxGraph : TypeAlias = networkx.MultiDiGraph
Coord : TypeAlias = tuple[float, float]   # (latitude, longitude)
def get_osmnx_graph() -> OsmnxGraph:
    ciutat = "Barcelona, Spain"
    graf = ox.graph_from_place(ciutat, network_type="all")
    
    return graf

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    # guarda el graf g al fitxer filename
    output_folder = "Desktop/PRACTICA2"
    

    ox.save_graph_shapefile(g, output_folder, filename)
    
def load_osmnx_graph(filename: str) -> OsmnxGraph: 
    # retorna el graf guardat al fitxer filename
    ruta_document = 'Desktop/PRACTICA2'
    graf = ox.load_graphml(ruta_document, filename)
    return graf

def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph: ...
    # retorna un graf fusió de g1 i g2
    


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: ...


def show(g: CityGraph) -> None: ...
    # mostra g de forma interactiva en una finestra
def plot(g: CityGraph, filename: str) -> None: ...
   # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename
def plot_path(g: CityGraph, p: Path, filename: str, ...) -> None: ...
    # mostra el camí p en l'arxiu filename
    
save_osmnx_graph(get_osmnx_graph(), 'graf_barcelona')
