from typing import TypeAlias
from dataclasses import dataclass
import json
import networkx as nx
import urllib.request
import staticmap
import os
import matplotlib.pyplot as plt
from PIL import Image
BusesGraph : TypeAlias = nx.Graph
Coord: TypeAlias = tuple[float,float]

@dataclass
class Parada:
    id: str
    pos: Coord
    def __init__(self,id:int,pos: Coord)->None:
        self.id = id
        self.pos = pos
        
class Bus:
    node_origen: Parada
    node_desti: Parada
    distancia: float
    info: str
    def __init__(self, node_origen: Parada, node_desti: Parada, distancia:float, info: str) -> None:
        self.node_origen = node_origen
        self.node_desti = node_desti
        self.distancia = distancia
        self.info = info
        
        
def distance(pos1:tuple[float,float], pos2:tuple[float,float]) -> float:
    d = (pos1[0] - pos2[0])**2 + \
            (pos1[1] - pos2[1])**2
    return d**(1/2)
       
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
    
                node_pos = (parada['UTM_X'], parada['UTM_Y'])

                # Afegir el node amb els atributs de nom i coordenades
                parada = Parada(id=node_id, pos = node_pos)
                graph.add_node(parada.id, pos=node_pos, node = parada)

    # Processar les arestes i afegir-les com a arestes amb els seus atributs corresponents
    for linia in data['ObtenirDadesAMBResult']['Linies']['Linia']:
        parades_linia = linia['Parades']['Parada']
        
                
        
        for i in range(len(parades_linia) - 1):
            dic_node_origen = parades_linia[i]
            dic_node_desti = parades_linia[i+1]
            if dic_node_origen['Municipi'] == 'Barcelona' and dic_node_desti['Municipi'] == 'Barcelona':
                node_origen_id = dic_node_origen['CodAMB']
                node_desti_id = dic_node_desti['CodAMB']
                node_origen_pos = (dic_node_origen['UTM_X'], dic_node_origen['UTM_Y'])
                node_desti_pos = (dic_node_desti['UTM_X'],dic_node_desti['UTM_Y'])
                    
                node_origen = Parada(id = node_origen_id, pos = node_origen_pos)
                node_desti = Parada(id = node_desti_id,pos = node_desti_pos)
                
            # Afegir l'aresta amb l'atribut de la línia de bus
            distancia = distance(node_origen.pos,node_desti.pos)
            edge = Bus(node_origen, node_desti, distancia, 'bus')
            if node_origen_id != node_desti_id:
                graph.add_edge(node_origen_id, node_desti_id, aresta = edge, length = distancia)   
    
    return graph

def show(g: BusesGraph) -> None:
    
    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw(g, pos=posicions, with_labels=False,font_size=5,node_size= 5)
    plt.show()
    
    
    
    
def plot(g: nx.Graph, nom_fitxer: str) -> None:
 # Crear un objecte StaticMap amb el mapa de fons de la ciutat
    city_map = staticmap.StaticMap(1000, 1000, url_template='https://a.tile.openstreetmap.org/{lat}/{lon}.png'.format(lat=41.3888, lon=2.159))

    # Afegir les parades com a marcadors al mapa
    for node_attrs in g.nodes.values():        
        parada = node_attrs['node']        
        city_map.add_marker(staticmap.CircleMarker(parada.pos, "red", 10))
    
    
    for edge_attrs in g.edges.values():        
        linia = edge_attrs['aresta']        
        line = staticmap.Line((linia.node_origen.pos, linia.node_desti.pos), "blue", 5)
        city_map.add_line(line)
    
    # Generar el mapa amb les parades i trajectes i desar el mapa com una imatge
    city_map.render().save(nom_fitxer)

   
def main()-> None:
    g = get_buses_graph()
    show(g)
    image_path = os.path.abspath('map.png')
    plot(g,"map.png")
    
if __name__=='__main__':
    main()
