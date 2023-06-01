import yogi
from city import *
from billboard import *
from rich.console import Console
from rich.table import Table
from rich.text import Text
from geopy.geocoders import Nominatim

def main() -> None:
    # mostrar el nom dels autors del projecte.
    console = Console()
    console.print("Benvingut!",
                  style="bold", highlight=True)

    cartellera = read()
    instruccions = [ "Opcions:",
        "1. Mostra el contingut de la cartellera",
        "2. Cerca a la cartellera",
        "3. Crea i mostra el graf de busos",
        "4. Crea i mostra el graf de ciutat",
        "5. Mostra el camí per anar a veure una pel·lícula",
        "6. Crèdits i noms dels autors del projecte",
        "7. Sortir"
    ]

    while True:
        for inst in instruccions:
            console.print(inst)
        console.print("Selecciona una opció: ", end='')
        opcio = input()
        # mostrar el contingut de la cartellera.
        if opcio == '1':
            escriu_cartellera(cartellera.projections())
        # cercar a la cartellera.
        elif opcio == '2':
            cerques = ["1. Pel·lícula", "2. Cinema", "3. Horari", "4. Combina",
                       "5. Cerca per mot", "6. Genere", "7. Actor", "8. Director"]
            for cerca in cerques:
                console.print(cerca)
            console.print("Què vols cercar? ", end='')
            cerca = yogi.read(int)
            if cerca == 1:
                sessions = cerca_pelicula(cartellera)
                if len(sessions) == 0:
                    text = Text.assemble(("Vaja! ", "red"), "La pel·lícula que has introduit no es troba a la cartellera. ",  (
                        "Assegura't d'escriure una que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                    console.print(text)

                else:
                    sort_hora(sessions)
                    escriu_cartellera(sessions)

            elif cerca == 2:
                sessions = cerca_cinema(cartellera)
                if not len(sessions):
                    text = Text.assemble(("Vaja! ", "red"), "El cinema que has introduit no es troba a la cartellera. ",  (
                        "Assegura't d'escriure'n un que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                    console.print(text)
                else:
                    sort_hora(sessions)
                    escriu_cartellera(sessions)

            elif cerca == 3:
                sessions = cerca_horari(cartellera)
                if len(sessions) == 0:
                    text = Text.assemble(
                        ("Vaja! ", "red"), "No hi ha cap pel·lícula programada per aquesta hora o no l'has escrit correctament.")
                    console.print(text)
                else:
                    sort_hora(sessions)
                    escriu_cartellera(sessions)

            elif cerca == 4:
                combos = ["1. Pel·lícula", "2. Cinema", "3. Horari"]
                for combo in combos:
                    console.print(combo)
                console.print(
                    "Escull els dos paràmetres amb els que vols cercar. ", end='')
                x, y = yogi.read(int), yogi.read(int)

                if x == 1:
                    sessions = cerca_pelicula(cartellera)
                    combinacio = combina(sessions, y)
                    escriu_cartellera(combinacio)

                elif x == 2:
                    sessions = cerca_cinema(cartellera)
                    combinacio = combina(sessions, y)
                    escriu_cartellera(combinacio)
                elif x == 3:
                    sessions = cerca_horari(cartellera)
                    combinacio = combina(sessions, y)
                    escriu_cartellera(combinacio)
                else:
                    console.print("Opció no vàlida", style="purple4")

            elif cerca == 5:
                console.print("Quin mot vols cercar? ", end='')
                mot = input()
                mots = cartellera.troba_mot(mot)
                sort_hora(mots)
                escriu_cartellera(mots)
            elif cerca == 6:
                console.print(
                    "Quin gènere vols cercar? Escrit en castellà.", end='')
                mot = input()
                mots = cartellera.troba_genere(mot)
                sort_hora(mots)
                escriu_cartellera(mots)
            elif cerca == 7:
                console.print("Quin actor vols cercar? ", end='')
                mot = input()
                mots = cartellera.troba_actor(mot)
                sort_hora(mots)
                escriu_cartellera(mots)
            elif cerca == 8:
                console.print("Quin director vols cercar? ", end='')
                mot = input()
                mots = cartellera.troba_director(mot)
                sort_hora(mots)
                escriu_cartellera(mots)

            else:
                console.print("Opció no vàlida", style="purple4")
        # mostrar el graf de busos.
        elif opcio == '3':
            busos = get_buses_graph()
            show(busos)
            console.print("Vols desar la imatge amb el mapa dels busos en un fitxer? ", end='')
            console.print("1. Sí", "2. No", end='\n')
            n = input()
            if n == '1':
                plot(busos, "graf_busos.png")
        # mostrar el graf de ciutat.
        elif opcio == '4':
            g1 = get_osmnx_graph()
            g2 = get_buses_graph()
            city = build_city_graph(g1, g2)
            show(city)
            console.print("Vols desar la imatge amb el mapa de la ciutat en un fitxer? ", end='')
            console.print("1. Sí", "2. No", end='\n')
            n = input()
            if n == '1':
                plot(city, "graf_barcelona.png")
        # # mostrar el camí per anar a veure una pel·lícula desitjada des d'un lloc donat en un moment donat. De totes les projeccions possibles cal mostrar el camí per arribar a la que comenci abans (i que s'hi pugui arribar a temps a peu i en bús).
        elif opcio == '5':
            geolocator = Nominatim(user_agent="geocoder_ap2")
            g1 = get_osmnx_graph()
            g2 = get_buses_graph()
            city = build_city_graph(g1, g2)
            sessions = cerca_pelicula(cartellera)
            escriu_cartellera(list(sessions))
            console.print("Escriu a quin cinema vols anar.")
            cine = input()
            sessions2 = combina(sessions, 2, cine)
            escriu_cartellera(list(sessions2))
            console.print("Des de quina adressa de Barcelona vols sortir?")
            adressa = input()
            coordenades : Coord = geolocator.geocode(adressa)
            if coordenades is not None:
                lat, lon = coordenades.latitude, coordenades.longitude
                console.print("Creant camí des de", adressa, "fins a", cinemes()[cine].address)
                cami = find_path(g1, city, (lon, lat), cinemes()[cine].coordenades)
                plot_path(city, cami, "cami_cinema.png")

        elif opcio == '6':
            console.print("Aleix Albaiges Torres i Gabriel Fortuny Carretero")
            
        elif opcio == '7':
            break

        else:
            console.print("Opció no vàlida", style="purple4")
        
    console.print("Adéu! Gràcies per visitar el nostre projecte. Aleix i Gabriel", style='magenta3')


def cerca_horari(cartellera: Billboard) -> list[Projection]:
    """Donada la cartellera es retorna la llista de projeccions a l'hora que es demana."""
    console = Console()
    console.print(
        "A quina Hora vols anar al cine? Escriu l'hora en punt. ", end='')
    pel = yogi.read(int)

    sessions = [x for x in cartellera.projections() if pel == x.time()[0]]
    return sessions


def cerca_pelicula(cartellera: Billboard) -> list[Projection]:
    """Donada la cartellera es retorna la llista de projeccions de la pel·licula que es demana."""
    console = Console()
    console.print("Quina Pel·licula vols cercar? ", end='')
    pel = input()

    sessions: list[Projection] = list()
    sessions = [x for x in cartellera.projections() if pel == x.film().title]
    return sessions


def combina(sessions: list[Projection], y: int, cine: str = '') -> list[Projection]:
    """Donades les sessions ja condicionades per un paràmetre, se les redueix al segon paràmetre i es retorna una llista de projeccions que compleixen ambdues restriccions."""
    console = Console()
    if y == 1:
        console.print("Quina Pel·licula vols cercar? ", end='')
        pel = input()
        combinacio = [
            x for x in sessions if x.film().title == pel]
        sort_hora(combinacio)
        return combinacio
    elif y == 2:
        
        if cine == '':
            console.print("A quin Cinema vols anar? ", end='')
            cine = input()
        combinacio = [
            x for x in sessions if x.cinema().name == cine]
        sort_hora(combinacio)
        return combinacio
    elif y == 3:
        console.print(
            "A quina Hora vols anar al cine? Escriu l'hora en punt. ", end='')
        pel = yogi.read(int)
        combinacio = [x for x in sessions if x.time()[
            0] == pel]
        sort_hora(combinacio)
        return combinacio
    else:
        console.print("Opció no vàlida", style="purple4")
        return list()


def cerca_cinema(cartellera: Billboard) -> list[Projection]:
    """Donada la cartellera es retorna la llista de projeccions que es duen a terme al cinema que es demana."""
    console = Console()
    console.print("A quin Cinema vols anar? ", end='')
    cine = input()

    sessions: list[Projection] = list()
    sessions = [x for x in cartellera.projections() if cine == x.cinema().name]

    return sessions


def escriu_cartellera(projeccions: list[Projection]) -> None:
    """Donada una llista de projeccions s'escriu en una taula del modul rich les sessions amb els elements: Titol, Cinema, Hora."""
    if len(projeccions):
        console = Console()
        taula = Table(title="Cartellera de Barcelona")
        taula.add_column("Pel·lícula")
        taula.add_column("Cinema")
        taula.add_column("Hora")
        for projeccio in projeccions:
            taula.add_row(projeccio.film().title, projeccio.cinema(
            ).name, f"{projeccio.time()[0]:02d}:{projeccio.time()[1]:02d}")
        console.print(taula)


if __name__ == '__main__':
    main()
