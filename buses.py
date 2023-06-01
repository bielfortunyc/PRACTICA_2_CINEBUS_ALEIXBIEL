from typing import TypeAlias
from dataclasses import dataclass
import json
import networkx as nx
import urllib.request
import staticmap
import matplotlib.pyplot as plt

BusesGraph : TypeAlias = nx.Graph

    
    
def get_buses_graph() -> nx.Graph:
    # Llegir les dades JSON
    url = 'https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json'
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    # Crear el graf de busos
    graph = nx.Graph()

   # Processar les parades i afegir-les com a nodes amb els seus atributs corresponents
    for i in range(len(data['ObtenirDadesAMBResult']['Linies']['Linia'])):
        parades = data['ObtenirDadesAMBResult']['Linies']['Linia'][i]['Parades']['Parada']
        for parada in parades:
            if parada['Municipi'] == 'Barcelona':
                node_id = int(parada['CodAMB'])
                node_lon, node_lat = parada['UTM_Y'], parada['UTM_X']

                # Afegir el node amb els atributs de nom i coordenades

                graph.add_node(node_id, pos=(node_lon,node_lat))

    # Processar les arestes i afegir-les com a arestes amb els seus atributs corresponents
    for linia in data['ObtenirDadesAMBResult']['Linies']['Linia']:
        parades_linia = linia['Parades']['Parada']
        
                
        
        for i in range(len(parades_linia) - 1):
            dic_node_origen = parades_linia[i]
            dic_node_desti = parades_linia[i+1]
            if dic_node_origen['Municipi'] == 'Barcelona' and dic_node_desti['Municipi'] == 'Barcelona':               
                node_origen_id = int(dic_node_origen['CodAMB'])
                node_desti_id = int(dic_node_desti['CodAMB'])
                
            # Afegir l'aresta amb l'atribut de la línia de bus
            if node_origen_id != node_desti_id:
                graph.add_edge(node_origen_id, node_desti_id)

    return graph

def show(g: BusesGraph) -> None:
    
    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos=posicions, with_labels=False,font_size=5,node_size= 5)
    plt.show()
    
    
    
    
def plot(g: nx.Graph, nom_fitxer: str) -> None:
# Crear un objecte StaticMap amb el mapa de fons de la ciutat
    city_map = staticmap.StaticMap(3500, 3500)

    # Afegir les parades com a marcadors al mapa
    for node in g.nodes:
        x, y = g.nodes[node]['pos']
        city_map.add_marker(staticmap.CircleMarker((x,y), "red", 6))

    # Afegir els trajectes com a línies al mapa
    for edge in g.edges:
        node1, node2 = edge
        x1, y1 = g.nodes[node1]['pos']
        x2, y2 = g.nodes[node2]['pos']
        line = staticmap.Line(((x1,y1),(x2,y2)), "blue", 2)

        city_map.add_line(line)
    # Generar el mapa amb les parades i trajectes
    image = city_map.render()

    # Desar el mapa com una imatge
    image.save(nom_fitxer)

def main()-> None:
    g = get_buses_graph()
    show(g)
    plot(g,"mapa_barcelona.png")
    
if __name__=='__main__':
    main()
