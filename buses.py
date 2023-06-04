from typing import TypeAlias
from dataclasses import dataclass
import json
import networkx as nx
import urllib.request
import staticmap
import matplotlib.pyplot as plt


BusesGraph: TypeAlias = nx.Graph


def get_buses_graph() -> BusesGraph:
    """A partir d'un fitxer JSON crea un graf de les línies de bus."""

    # Llegir les dades JSON
    url = 'https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json'
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    graph: BusesGraph = nx.Graph()

    # Processar les parades i afegir-les com a
    # nodes amb els seus atributs corresponents
    for i in range(len(data['ObtenirDadesAMBResult']['Linies']['Linia'])):
        parades = data['ObtenirDadesAMBResult']['Linies']['Linia'][i][
            'Parades']['Parada']

        for parada in parades:
            if parada['Municipi'] == 'Barcelona':
                node_id = int(parada['CodAMB'])
                node_lon, node_lat = parada['UTM_Y'], parada['UTM_X']

                # Afegir el node amb els atributs d'id i de coordenades
                graph.add_node(node_id, pos=(
                    node_lon, node_lat), tipus="Parada")

    # Processar les arestes i afegir-les com a arestes
    # amb els seus atributs corresponents
    for linia in data['ObtenirDadesAMBResult']['Linies']['Linia']:
        parades_linia = linia['Parades']['Parada']

        for i in range(len(parades_linia) - 1):
            dic_node_origen = parades_linia[i]
            dic_node_desti = parades_linia[i+1]
            if dic_node_origen['Municipi'] == 'Barcelona' \
                    and dic_node_desti['Municipi'] == 'Barcelona':
                node_origen_id = int(dic_node_origen['CodAMB'])
                node_desti_id = int(dic_node_desti['CodAMB'])

            # Afegir l'aresta amb l'atribut de la línia de bus
            if node_origen_id != node_desti_id:
                graph.add_edge(node_origen_id, node_desti_id, tipus="Bus")

    return graph


def show_buses(g: BusesGraph) -> None:
    """Mostra el graf g per pantalla."""

    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos=posicions, with_labels=False, font_size=5, node_size=5)
    plt.show()


def plot_buses(g: BusesGraph, filename: str) -> None:
    """
    Desa g com una imatge amb el mapa de la
    ciutat de fons en l'arxiu filename.
    """
    # Mostra el camí p en l'arxiu filename
    map = staticmap.StaticMap(3500, 3500)

    # Afegir les parades com a marcadors al mapa
    for node in g.nodes:
        x, y = g.nodes[node]['pos']
        map.add_marker(
            staticmap.CircleMarker((x, y), "black", 15))

    # Afegir els trajectes com a línies al mapa
    for u, v, data in g.edges(data=True):
        x1, y1 = g.nodes[u]['pos']
        x2, y2 = g.nodes[v]['pos']
        line = staticmap.Line(((x1, y1), (x2, y2)), "red", 15)
        map.add_line(line)

    # Generar el mapa amb les parades i trajectes
    image = map.render()

    image.show(filename)

    # Desar el mapa com una imatge
    image.save(filename)
