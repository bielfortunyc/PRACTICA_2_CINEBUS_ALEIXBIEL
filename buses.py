from typing import TypeAlias
from dataclasses import dataclass
import json
import networkx as nx
import urllib.request

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
        parades = data['ObtenirDadesAMBResult']['Linies']['Linia'][i]
        ['Parades']['Parada']

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
