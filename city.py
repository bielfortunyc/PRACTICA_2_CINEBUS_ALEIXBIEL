import networkx as nx
from typing import TypeAlias, Optional
import osmnx as ox
import pickle
import matplotlib.pyplot as plt
import os
from buses import *
from haversine import haversine, Unit

CityGraph : TypeAlias = nx.Graph
OsmnxGraph : TypeAlias = nx.MultiDiGraph
Coord: TypeAlias = tuple[float,float]
Path: TypeAlias = nx.Graph
    
def keep_first_edge_del_geometry(graf: OsmnxGraph) -> OsmnxGraph:
    for u, v, key, geom in graf.edges(data = "geometry", keys = True):
            if geom is not None:
                del(graf[u][v][key]["geometry"])
        
def get_osmnx_graph() -> OsmnxGraph:
    filename = 'graf_barcelona'
    if os.path.exists(filename):
        return load_osmnx_graph(filename)
    else:
        ciutat = "Barcelona"
        multi_graf = ox.graph_from_place(ciutat, network_type='walk', simplify=True)
        for u, v, key, geom in multi_graf.edges(data = "geometry", keys = True):
            if geom is not None:
                del(multi_graf[u][v][key]["geometry"])
        save_osmnx_graph(multi_graf,"graf_barcelona")
        return multi_graf

def save_osmnx_graph(g: OsmnxGraph, filename: str) -> None:
    # guarda el graf g al fitxer filename
    # Obtenir el directori actual
    current_dir = os.getcwd()

    # Definir la ruta del fitxer de sortida
    output_folder = os.path.join(current_dir, filename)
    with open(output_folder, 'wb') as file:
        pickle.dump(g, file)

    
def load_osmnx_graph(filename: str) -> OsmnxGraph: 
    # retorna el graf guardat al fitxer filename
      # Obtenir el directori actual
    current_dir = os.getcwd()

    # Definir la ruta del fitxer
    ruta_document = os.path.join(current_dir, filename)

    # Comprovar si el fitxer existeix
    if not os.path.exists(ruta_document):
        raise FileNotFoundError(f"El fitxer '{filename}' no existeix en el directori actual.")

    # Llegir el graf des del fitxer
    with open(ruta_document, 'rb') as file:
        graf = pickle.load(file)
    return graf

def distance(n1_coord: tuple[float,float], n2_coord: tuple[float, float]) -> float:
    return haversine(n1_coord, n2_coord, unit = Unit.METERS)

#def distance_(n1_lat: float, n1_lon: float, n2_lat: float, n2_lon: float) -> float:
    d = (n1_lat - n2_lat)**2 + \
            (n1_lon - n2_lon)**2
    return d**(1/2)
def build_city_graph(g1: OsmnxGraph, g2: BusesGraph) -> CityGraph:
    # retorna un graf fusió de g1 i g2
    
    city_graph = nx.Graph()
    velocitat_bus = 5
    velocitat_caminant = 1.9
    for node_id, data in g1.nodes(data=True):
        city_graph.add_node(node_id, pos = (data['x'],data['y']), tipus = "Cruilla")
    
    for u, v, data in g1.edges(data=True):
        if u != v:      
            city_graph.add_edge(u,v, weight= data['length']/velocitat_caminant, tipus = "Carrer")
    
    llista_pos_lat: list[tuple[float]] = []
    llista_pos_lon: list[tuple[float]] = []
    
    for node_id, data in g2.nodes(data = True):
        city_graph.add_node(node_id, pos = data['pos'], tipus = "Parada")
        llista_pos_lon.append(data['pos'][0])
        llista_pos_lat.append(data['pos'][1])
        
    
    cruilles_properes = ox.distance.nearest_nodes(g1, llista_pos_lon,llista_pos_lat, return_dist = False)
    dict_parada_cruilla_corresponent: dict[int,int] = dict()
    for i, id in enumerate(g2.nodes):
        cruilla_propera_corresponent = cruilles_properes[i]
        dict_parada_cruilla_corresponent[id] = cruilla_propera_corresponent
        if id != cruilla_propera_corresponent:
            
            
            city_graph.add_edge(id,cruilla_propera_corresponent, tipus = "Carrer")        
    
    
    for u, v, data in g2.edges(data = True):
        origen = dict_parada_cruilla_corresponent[u]
        desti = dict_parada_cruilla_corresponent[v]
        shortest_path = ox.distance.shortest_path(g1, orig = origen, dest = desti, weight = 'weight')
        pes : float = (distance(g2.nodes[u]['pos'],city_graph.nodes[origen]['pos']) + \
            distance(g2.nodes[v]['pos'],city_graph.nodes[desti]['pos'])) / velocitat_caminant
        for i in range(len(shortest_path)-1):
            id = shortest_path[i]
            next_id = shortest_path[i+1]
            try:
                pes += city_graph[id][next_id]['weight']/velocitat_bus
            except:
                print(g1[id][next_id])
         
        city_graph.add_edge(u, v, weight = pes, tipus = 'Bus')
        
        
        
    return city_graph


def find_path(ox_g: OsmnxGraph, g: CityGraph, src: Coord, dst: Coord) -> Path: 
    src_node = ox.distance.nearest_nodes(ox_g, src[1], src[0])
    dst_node = ox.distance.nearest_nodes(ox_g, dst[1], dst[0])
    shortest_path = ox.distance.shortest_path(g, orig = src_node, dest = dst_node, weight = 'weight')
    path = nx.Graph()
    for i in range(len(shortest_path)-1):
        id = shortest_path[i]
        pos = (g.nodes[id]['pos'])
        
        path.add_node(id, pos = pos, tipus = g.nodes[id]['tipus'])
        next_id = shortest_path[i+1]
        if 'weight' in g[id][next_id]:
            weight = g[id][next_id]['weight']
            path.add_edge(id, next_id,weight = weight, tipus = g[id][next_id]['tipus'])
        else: 
            path.add_edge(id, next_id, tipus = g[id][next_id]['tipus'])
            
        
    ultim_id = shortest_path[-1]
    path.add_node(ultim_id, pos = (g.nodes[ultim_id]['pos']), tipus = g.nodes[ultim_id]['tipus'])
    return path

def total_time_path(p : Path) -> float:
    temps = 0
    for u, v, data in p.edges(data = True):
        if 'weight' in data:
            temps += data['weight']
            
    return temps
    
    

def show(g: CityGraph) -> None:
    # mostra g de forma interactiva en una finestra
    posicions = nx.get_node_attributes(g, 'pos')
    nx.draw_networkx(g, pos=posicions, node_size=10, with_labels=False)
    plt.show()
    
def plat(g: CityGraph, filename: str) -> None:
   # desa g com una imatge amb el mapa de la cuitat de fons en l'arxiu filename
   ...
def plot_path(g: CityGraph, p: Path, filename: str) -> None: 
    
    # mostra el camí p en l'arxiu filename
    path_map = staticmap.StaticMap(3500, 3500)

    # Afegir les parades com a marcadors al mapa
    for node in p.nodes:
        x, y = p.nodes[node]['pos']
        try:
            if p.nodes[node]['tipus'] == "Cruilla":
                path_map.add_marker(staticmap.CircleMarker((x,y), "black", 15))
            else:
                path_map.add_marker(staticmap.CircleMarker((x,y), "blue", 15))
        except KeyError:
            print(node, p.nodes[node])
            
    # Afegir els trajectes com a línies al mapa
    for u, v, data in p.edges(data = True):
        x1, y1 = p.nodes[u]['pos']
        x2, y2 = p.nodes[v]['pos']
        

        if data['tipus'] == "Carrer":
            line = staticmap.Line(((x1,y1),(x2,y2)), "red", 15)
        else: 
            line = staticmap.Line(((x1,y1),(x2,y2)), "green", 15)
        

        path_map.add_line(line)
    # Generar el mapa amb les parades i trajectes
    image = path_map.render()

    # Desar el mapa com una imatge
    image.save(filename)
    
def main() -> None:
    
    
    g1 = get_osmnx_graph()
    g2 = get_buses_graph()
    city = build_city_graph(g1, g2)
    
    
    #show(city)
    #plot(city,"map_barcelona.png")
    path = find_path(g1, city, (41.4101085,2.2172596), (41.386218, 2.162393))
    #print(distance((41.4097177,2.1640022), (41.409576, 2.163956)))
    print(path.edges(data=True))
    print(total_time_path(path))
    #plot_path(city, path, "path_proper.png")
if __name__ ==  '__main__':
    main()
