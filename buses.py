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
