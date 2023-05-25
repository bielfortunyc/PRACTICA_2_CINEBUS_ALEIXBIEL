from typing import TypeAlias
from dataclasses import dataclass
import json
import networkx as nx
import urllib.request
import staticmaps
import matplotlib.pyplot as plt

BusesGraph : TypeAlias = nx.Graph

@dataclass
class Bus:
    id: int
    nom: str
    x: float
    y: float
    def __init__(self,id:int,nom:str,x:float,y:float)->None:
        self.id = id
        self.nom = nom
        self.x = x
        self.y = y
    
    
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
                node_id = parada['CodAMB']
                node_nom = parada['Nom']
                node_x, node_y = parada['UTM_X'], parada['UTM_Y']

                # Afegir el node amb els atributs de nom i coordenades
                bus = Bus(id=node_id,nom=node_nom,x=node_x,y=node_y)
                graph.add_node(bus.id, pos=(node_x,node_y))

    # Processar les arestes i afegir-les com a arestes amb els seus atributs corresponents
    for linia in data['ObtenirDadesAMBResult']['Linies']['Linia']:
        parades_linia = linia['Parades']['Parada']
        
                
        
        for i in range(len(parades_linia) - 1):
            if parades_linia[i]['Municipi'] == 'Barcelona' and parades_linia[i+1]['Municipi'] == 'Barcelona':
                node_origen = parades_linia[i]['CodAMB']
                node_desti = parades_linia[i + 1]['CodAMB']
                linia_bus = linia['Nom']

            # Afegir l'aresta amb l'atribut de la línia de bus
            graph.add_edge(node_origen, node_desti, linia=linia_bus)

    return graph

def show(g: BusesGraph) -> None:
    
    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos=posicions, with_labels=False,font_size=5,node_size= 5)
    plt.show()
    
    
    
    
def plot(g: nx.Graph, nom_fitxer: str) -> None:
# Crear un objecte StaticMap amb el mapa de fons de la ciutat
    city_map = staticmaps.StaticMap(800, 800)
    city_map.add_image_layer(staticmaps.ImageLayer(nom_fitxer))

    # Afegir les parades com a marcadors al mapa
    for node in g.nodes:
        x, y = g.nodes[node]['pos']
        marker = staticmaps.Marker(staticmaps.create_latlng(x, y))
        city_map.add_marker(marker)
    # Afegir els trajectes com a línies al mapa
    for edge in g.edges:
        node1, node2 = edge
        x1, y1 = g.nodes[node1]['pos']
        x2, y2 = g.nodes[node2]['pos']
        line = staticmaps.Line([staticmaps.create_latlng(x1, y1), staticmaps.create_latlng(x2, y2)], 'blue', 3)
        city_map.add_line(line)
    # Generar el mapa amb les parades i trajectes
    image = city_map.render()

    # Desar el mapa com una imatge
    image.save(nom_fitxer)

def main()-> None:
    g = get_buses_graph()
    #show(g)
    plot(g,"mapa_barcelona.png")
    
if __name__=='__main__':
    main()
