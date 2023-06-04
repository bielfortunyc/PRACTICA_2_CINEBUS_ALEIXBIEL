import networkx as nx
from typing import TypeAlias
import osmnx as ox
import pickle
import matplotlib.pyplot as plt
import staticmap
import os
from buses import *
from haversine import haversine, Unit

CityGraph: TypeAlias = nx.Graph
OsmnxGraph: TypeAlias = nx.MultiDiGraph
Coord: TypeAlias = tuple[float, float]
Path: TypeAlias = nx.Graph


def get_osmnx_graph() -> OsmnxGraph:
    """
    Comprova si existeix el graf de Barcelona, si es dona el
    cas el càrrega i si no el crea i el guarda.
    """

    filename = 'graf_barcelona'
    if os.path.exists(filename):
        return load_osmnx_graph(filename)
    else:
        ciutat = "Barcelona"
        multi_graf = ox.graph_from_place(
            ciutat, network_type='walk', simplify=True)
        for u, v, key, geom in multi_graf.edges(data="geometry", keys=True):
            if geom is not None:
                del (multi_graf[u][v][key]["geometry"])
        save_osmnx_graph(multi_graf, "graf_barcelona")
        return multi_graf


def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    """Guarda el graf 'g' al fitxer 'filename'."""

    # Obtenir el directori actual
    current_dir = os.getcwd()

    # Definir la ruta del fitxer de sortida
    output_folder = os.path.join(current_dir, filename)
    with open(output_folder, 'wb') as file:
        pickle.dump(g, file)


def load_osmnx_graph(filename: str) -> OsmnxGraph:
    """
    Carrega el graf des del fitxer 'filename' i
    el retorna com un objecte OsmnxGraph.

    """

    # Obtenir el directori actual
    current_dir = os.getcwd()

    # Definir la ruta del fitxer
    ruta_document = os.path.join(current_dir, filename)

    # Comprovar si el fitxer existeix
    if not os.path.exists(ruta_document):
        raise FileNotFoundError(
            f"El fitxer '{filename}' no existeix en el directori actual.")

    # Llegir el graf des del fitxer
    with open(ruta_document, 'rb') as file:
        graf = pickle.load(file)
    return graf


def distance(n1_coord: Coord, n2_coord: Coord) -> float:
    """Retorna la distància sobre una esfera de dues coordenades en metres."""

    return haversine(n1_coord, n2_coord, unit=Unit.METERS)


def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
    """Retorna un graf fusió de g1 i g2"""

    city_graph: CityGraph = nx.Graph()
    velocitat_bus: float = 5.1
    velocitat_caminant: float = 1.9

    for node_id, data in g1.nodes(data=True):
        city_graph.add_node(node_id, pos=(
            data['x'], data['y']), tipus="Cruilla")

    for u, v, data in g1.edges(data=True):
        if u != v:
            city_graph.add_edge(
                u, v, weight=data['length']/velocitat_caminant, tipus="Carrer")

    llista_pos_lat: list[float] = []
    llista_pos_lon: list[float] = []

    for node_id, data in g2.nodes(data=True):
        city_graph.add_node(node_id, pos=data['pos'], tipus="Parada")
        llista_pos_lon.append(data['pos'][0])
        llista_pos_lat.append(data['pos'][1])

    # S'obtè una llista amb els id de les cruïlles més properes
    # a cada una de les Coord que se li passa en la llista paràmetre
    cruilles_properes = ox.distance.nearest_nodes(
        g1, llista_pos_lon, llista_pos_lat, return_dist=False)

    # Es declara un diccionari que consistirà de id de parades
    # com a claus i id de la cruïlla propera com a valor.
    dict_parada_cruilla_corresponent: dict[int, int] = dict()

    for i, id in enumerate(g2.nodes):
        cruilla_propera_corresponent = cruilles_properes[i]
        dict_parada_cruilla_corresponent[id] = cruilla_propera_corresponent
        if id != cruilla_propera_corresponent:
            city_graph.add_edge(
                id, cruilla_propera_corresponent, tipus="Carrer")

    for u, v, data in g2.edges(data=True):
        origen = dict_parada_cruilla_corresponent[u]
        desti = dict_parada_cruilla_corresponent[v]

        # Es calcula el camí més curt que es pot fer entre les cruïlles
        # més properes a dues parades.
        shortest_path = ox.distance.shortest_path(
            g1, orig=origen, dest=desti, weight='weight')

        pos_u = g2.nodes[u]['pos']
        pos_u_cruilla = city_graph.nodes[origen]['pos']
        pos_v = g2.nodes[v]['pos']
        pos_v_cruilla = city_graph.nodes[desti]['pos']
        # Al pes entre els busos s'afegeix la distància a vol d'ocell
        # entre la parada inicial i final i les seves corresponents
        # cruïlles tot dividint per la velocitat caminant.
        pes: float = (distance(pos_u, pos_u_cruilla) +
                      distance(pos_v, pos_v_cruilla)) / velocitat_caminant

        # Afegir el pes dels carrers per fer el camí.
        for i in range(len(shortest_path)-1):
            id = shortest_path[i]
            next_id = shortest_path[i+1]
            pes += city_graph[id][next_id]['weight']/velocitat_bus

        city_graph.add_edge(u, v, weight=pes, tipus='Bus')

    return city_graph


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path:
    """
    Troba el camí més curt per anar des d'unes coordenades
    origen fins a unes coordenades destí.

    """

    src_node = ox.distance.nearest_nodes(ox_g, src[1], src[0])
    dst_node = ox.distance.nearest_nodes(ox_g, dst[1], dst[0])

    shortest_path = ox.distance.shortest_path(
        g, orig=src_node, dest=dst_node, weight='weight')

    # Crear un graf amb els nodes i les arestes del camí més curt.
    path = nx.Graph()
    for i in range(len(shortest_path)-1):
        id = shortest_path[i]
        pos = (g.nodes[id]['pos'])
        path.add_node(id, pos=pos, tipus=g.nodes[id]['tipus'])

        next_id = shortest_path[i+1]
        if 'weight' in g[id][next_id]:
            weight = g[id][next_id]['weight']
            path.add_edge(id, next_id, weight=weight,
                          tipus=g[id][next_id]['tipus'])
        else:
            path.add_edge(id, next_id, tipus=g[id][next_id]['tipus'])

    ultim_id = shortest_path[-1]
    path.add_node(ultim_id, pos=(
        g.nodes[ultim_id]['pos']), tipus=g.nodes[ultim_id]['tipus'])
    return path


def total_time_path(p: Path) -> float:
    """Retorna el temps total que es triga a recórrer un camí."""

    temps = 0
    for u, v, data in p.edges(data=True):
        if 'weight' in data:
            temps += data['weight']

    return temps


def show(g: nx.Graph) -> None:
    """Mostra el graf g per pantalla."""

    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos=posicions, with_labels=False, font_size=5, node_size=5)
    plt.show()


def plot(g: nx.Graph, filename: str) -> None:
    """
    Desa g com una imatge amb el mapa de la
    ciutat de fons en l'arxiu filename.
    """
    # Mostra el camí p en l'arxiu filename
    map = staticmap.StaticMap(3500, 3500)

    # Afegir les parades com a marcadors al mapa
    for node in g.nodes:
        x, y = g.nodes[node]['pos']
        if g.nodes[node]['tipus'] == "Cruilla":
            map.add_marker(
                staticmap.CircleMarker((x, y), "black", 15))
        else:
            map.add_marker(staticmap.CircleMarker((x, y), "blue", 15))

    # Afegir els trajectes com a línies al mapa
    for u, v, data in g.edges(data=True):
        x1, y1 = g.nodes[u]['pos']
        x2, y2 = g.nodes[v]['pos']

        if data['tipus'] == "Carrer":
            line = staticmap.Line(((x1, y1), (x2, y2)), "red", 15)
        else:
            line = staticmap.Line(((x1, y1), (x2, y2)), "green", 15)

        map.add_line(line)
    # Generar el mapa amb les parades i trajectes
    image = map.render()

    image.show(filename)

    # Desar el mapa com una imatge
    image.save(filename)
