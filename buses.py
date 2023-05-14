from typing import TypeAlias
from dataclasses import dataclass
import json
import networkx as nx
import urllib.request
import staticmaps
import matplotlib.pyplot as plt

BusesGraph : TypeAlias = nx.Graph

@dataclass
class Stop:
    id: str
    name: str
    lat: float
    lon: float
    type: str

@dataclass
class Route:
    start_stop: str
    end_stop: str
    bus_line: str
    
def get_buses_graph() -> nx.Graph:
    # Llegir les dades JSON
    url = 'https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json'
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    # Crear el graf de busos
    graph = nx.Graph()

    # Afegir nodes al graf
    for stop in data['parades']:
        stop_id = stop['idParada']
        stop_name = stop['nomParada']
        stop_lat = stop['coordenades']['lat']
        stop_lon = stop['coordenades']['lon']
        stop_type = stop['tipusParada']
        stop_obj = Stop(id=stop_id, name=stop_name, lat=stop_lat, lon=stop_lon, type=stop_type)
        graph.add_node(stop_id, **stop_obj.__dict__)
    
    for line in data['linies']:
        stops = line['parades']
        for i in range(len(stops) - 1):
            start_stop_id = stops[i]['idParada']
            end_stop_id = stops[i + 1]['idParada']
            bus_line = line['codiLinia']
            route_obj = Route(start_stop=start_stop_id, end_stop=end_stop_id, bus_line=bus_line)
            graph.add_edge(start_stop_id, end_stop_id, **route_obj.__dict__)
            
    return graph

def show(g: BusesGraph) -> None:
    # Crear gràfic de NetworkX a partir del graf de busos
    nx_graph = nx.Graph(g)

    # Dibuixar el gràfic de NetworkX
    pos = {node_id: (g.nodes[node_id]['lon'], g.nodes[node_id]['lat']) for node_id in g.nodes}
    nx.draw(nx_graph, pos, with_labels=True)
    plt.show()

def plot(g: BusesGraph, nom_fitxer: str) -> None:
    # Crear mapa amb les parades dels autobusos
    mapa = staticmaps.StaticMap(800, 600)
    for node_id in g.nodes:
        lon, lat = g.nodes[node_id]['lon'], g.nodes[node_id]['lat']
        pos = staticmaps.create_latlng(lat, lon)
        marker = staticmaps.Marker(pos)
        mapa.add_marker(marker)

    # Afegir el mapa de la ciutat de fons
    ciutat = staticmaps.StaticMap(800, 600)
    ciutat.add_image(staticmaps.Image(nom_fitxer), 0, 0, 800, 600)

    # Unir els mapes
    mapa.render()
    ciutat.add_image(mapa.image, 0, 0, 800, 600)

    # Desar el mapa com una imatge
    ciutat.save('mapa.png')
