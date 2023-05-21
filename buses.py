from dataclasses import dataclass
import json
import networkx as nx
import urllib.request
import staticmaps as sm
import matplotlib.pyplot as plt



    
def get_buses_graph() -> nx.Graph:
    # Llegir les dades JSON
    url = 'https://www.ambmobilitat.cat/OpenData/ObtenirDadesAMB.json'
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    # Crear el graf de busos
    graph = nx.Graph()

   # Processar les parades i afegir-les com a nodes amb els seus atributs corresponents
    parades = data['ObtenirDadesAMBResult']['Linies']['Linia'][0]['Parades']['Parada']
    for parada in parades:
        node_id = parada['CodAMB']
        node_nom = parada['Nom']
        coordenades = (parada['UTM_X'], parada['UTM_Y'])

        # Afegir el node amb els atributs de nom i coordenades
        graph.add_node(node_id, nom=node_nom, coordenades=coordenades)

    # Processar les arestes i afegir-les com a arestes amb els seus atributs corresponents
    for linia in data['ObtenirDadesAMBResult']['Linies']['Linia']:
        parades_linia = linia['Parades']['Parada']
        for i in range(len(parades_linia) - 1):
            node_origen = parades_linia[i]['CodAMB']
            node_desti = parades_linia[i + 1]['CodAMB']
            linia_bus = linia['Nom']

            # Afegir l'aresta amb l'atribut de la línia de bus
            graph.add_edge(node_origen, node_desti, linia=linia_bus)

    return graph

def show(g: nx.Graph) -> None:
    nx.draw(g, with_labels=False,node_size= 5)
    plt.show()
def plot(g: nx.Graph, nom_fitxer: str) -> None:
# Crear un objecte StaticMap amb el mapa de fons de la ciutat
    city_map = sm.StaticMap(800, 800)
    city_map.add_image_layer(sm.ImageLayer(nom_fitxer))

    # Afegir les parades com a marcadors al mapa
    for node in g.nodes:
        lat, lon = g.nodes[node]['coordenades']
        marker = sm.Marker(sm.create_latlng(lat, lon))
        city_map.add_marker(marker)

    # Afegir els trajectes com a línies al mapa
    for edge in g.edges:
        node1, node2 = edge
        lat1, lon1 = g.nodes[node1]['coordenades']
        lat2, lon2 = g.nodes[node2]['coordenades']
        line = sm.Line([sm.create_latlng(lat1, lon1), sm.create_latlng(lat2, lon2)], 'blue', 3)
        city_map.add_line(line)

    # Generar el mapa amb les parades i trajectes
    image = city_map.render()

    # Desar el mapa com una imatge
    image.save(nom_fitxer)

def main()-> None:
	g = get_buses_graph()
	show(g)
	plot(g,"Mapa-turistico-de-Barcelona.png")
    
if __name__=='__main__':
    main()
