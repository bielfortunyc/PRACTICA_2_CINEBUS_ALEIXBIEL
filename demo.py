import yogi
from city import *
from billboard import *
from rich.console import Console
from rich.table import Table
from rich.text import Text
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta


def main() -> None:
    console = Console()
    clear()
    console.print("Benvingut!",
                  style="aquamarine1 bold", highlight=True)

    cartellera = read() # S'inicialitzen la cartellera i els grafs al principi, doncs així no s'han d'inicialitza per cada cerca que es vulgui fer.
    g1 = get_osmnx_graph()
    g2 = get_buses_graph()
    city = build_city_graph(g1, g2)

    instruccions = ["1. Mostra el contingut de la cartellera",
                    "2. Cerca a la cartellera",
                    "3. Crea i mostra el graf de busos",
                    "4. Crea i mostra el graf de ciutat",
                    "5. Mostra el camí per anar a veure una pel·lícula",
                    "6. Crèdits i noms dels autors del projecte",
                    "7. Sortir"
                    ]

    while True:
        taula = Table()
        taula.add_column("Opcions")
        for inst in instruccions:
            taula.add_row(inst, style='cyan2 bold')
        console.print(taula)
        console.print("Escull una opció: ", style="light_pink3", end='')
        opcio = input()
        clear()
        # mostrar el contingut de la cartellera.
        if opcio == '1':
            escriu_cartellera(cartellera.projections())
        # cercar a la cartellera.
        elif opcio == '2':
            cerques = ["1. Pel·lícula", "2. Cinema", "3. Horari", "4. Combina",
                       "5. Cerca per mot", "6. Genere", "7. Actor", "8. Director"]
            taula = Table()
            taula.add_column("Cerques")
            for cerca in cerques:
                taula.add_row(cerca, style='dark_turquoise')
            console.print(taula)
            console.print("Què vols cercar? ", style="light_pink3", end='')
            cerca = input()
            if cerca == '1':
                sessions = cartellera.cerca_pelicula()
                if not len(sessions):
                    text = Text.assemble(("Vaja! ", "red"), "La pel·lícula que has introduit no es troba a la cartellera. ",  (
                        "Assegura't d'escriure una que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                    console.print(text)

                else:
                    clear()
                    film = sessions[0].film()
                    console.print("Projeccions de", film.title, style="yellow2")
                    console.print("Gèneres:", *film.genre, style="yellow2")
                    console.print("Actors i actrius:", *film.actors, style="yellow2")
                    console.print("Director/s:", *film.director, style="yellow2")
                    console.print()
                    escriu_cartellera(sessions)

            elif cerca == '2':
                sessions = cartellera.cerca_cinema()
                if not len(sessions):
                    text = Text.assemble(("Vaja! ", "red"), "El cinema que has introduit no es troba a la cartellera. ",  (
                        "Assegura't d'escriure'n un que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                    console.print(text)
                else:
                    clear()
                    cine = sessions[0].cinema()
                    console.print("Projeccions a", cine.name, style="yellow2")
                    console.print("Adreça:", cine.address, style="yellow2")
                    console.print()
                    escriu_cartellera(sessions)

            elif cerca == '3':
                sessions = cartellera.cerca_horari()
                if not len(sessions):
                    text = Text.assemble(
                        ("Vaja! ", "red"), "No hi ha cap pel·lícula programada per aquesta hora o no l'has escrit correctament.")
                    console.print(text)
                else:
                    clear()
                    hora = sessions[0].time()
                    console.print("Projeccions a les",
                                  f"{hora[0]:02d}:{hora[1]:02d}", style="yellow2")
                    console.print()
                    escriu_cartellera(sessions)

            elif cerca == '4':
                combos = ["1. Pel·lícula", "2. Cinema", "3. Horari"]
                taula = Table()
                taula.add_column('Combinacions')
                for combo in combos:
                    taula.add_row(combo, style='green4')
                console.print(taula)
                console.print(
                    "Escull els dos paràmetres amb els que vols cercar. ", end='')
                try:
                    x, y = yogi.read(int), yogi.read(int)
                    clear()
                    if x == 1:
                        sessions = cartellera.cerca_pelicula()
                        combinacio = combina(sessions, y)
                        film = combinacio[0].film()
                        if len(combinacio):
                            console.print("Projeccions de", film.title, style="yellow2")
                            console.print("Gèneres:", *film.genre, style="yellow2")
                            console.print("Actors i actrius:", *film.actors, style="yellow2")
                            console.print("Director/s:", *film.director, style="yellow2")
                            console.print()

                    elif x == 2:
                        sessions = cartellera.cerca_cinema()
                        combinacio = combina(sessions, y)
                        if len(combinacio):
                            console.print("Projeccions a",
                                          combinacio[0].cinema().name, style="yellow2")
                            console.print(
                                "Adreça:", combinacio[0].cinema().address, style="yellow2")
                            console.print()

                    elif x == 3:
                        sessions = cartellera.cerca_horari()
                        combinacio = combina(sessions, y)
                        if len(combinacio):
                            hora = combinacio[0].time()
                            console.print("Projeccions a les",
                                          f"{hora[0]:02d}:{hora[1]:02d}", style="yellow2")
                            console.print()

                    else:
                        console.print("Opció no vàlida", style="purple4")
                    if len(combinacio):
                        escriu_cartellera(combinacio)
                    else:
                        text = Text.assemble(
                            ("Vaja! ", "red"), "No hi ha cap combinació amb els paràmetres donats.")
                        console.print(text)
                except:
                    console.print("Opció no vàlida", style="purple4")

            elif cerca == '5':
                console.print("Quin mot vols cercar? ", end='')
                mot = input()
                mots = cartellera.troba_mot(mot)
                if len(mots):
                    clear()
                    console.print("Pel·icules amb el mot",
                                  mot, style='deep_pink3')
                    escriu_cartellera(mots)
                else:
                    text = Text.assemble(
                        ("Vaja! ", "red"), "No hi ha cap pel·lícula o cinema amb el mot escrit.")
                    console.print(text)
            elif cerca == '6':
                taula = Table()
                generes = ['Acción', 'Animación', 'Aventura', 'Biografía', 'Ciencia ficción', 'Comedia', 'Comedia dramática', 'Comedia musical', 'Crimen',
                           'Documental', 'Drama', 'Familia', 'Fantasía', 'Guerra', 'Histórico', 'Judicial', 'Musical', 'Romántico', 'Suspense', 'Terror', 'Western']
                taula.add_column("Gèneres")
                for genre in generes:
                    taula.add_row(genre, style='medium_purple2')
                console.print(taula)
                console.print(
                    "Quin gènere vols cercar? Escrit en castellà. ", end='', style='medium_purple2')
                mot = input()
                mots = cartellera.troba_genere(mot)
                if len(mots):
                    clear()
                    console.print("Pel·icules amb el gènere",
                                  mot, style='deep_pink3')
                    console.print()
                    escriu_cartellera(mots)
                else:
                    text = Text.assemble(
                        ("Vaja! ", "red"), "No hi ha cap pel·lícula amb el gènere escrit o no s'ha escrit correctament.")
                    console.print(text)
            elif cerca == '7':
                console.print("Quin actor vols cercar? ", end='', style='medium_purple2')
                mot = input()
                mots = cartellera.troba_actor(mot)
                if len(mots):
                    clear()
                    console.print("Pel·icules amb l'actor o actriu",
                                  mot, style='deep_pink3')
                    console.print()
                    escriu_cartellera(mots)
                else:
                    text = Text.assemble(
                        ("Vaja! ", "red"), "No hi ha cap pel·lícula amb el nom de l'actor que has escrit. Revisa haver-lo escrit correctament.")
                    console.print(text)
            elif cerca == '8':
                console.print("Quin director vols cercar? ", end='')
                mot = input()
                mots = cartellera.troba_director(mot)
                if len(mots):
                    clear()
                    console.print("Pel·icules amb el director/a",
                                  mot, style='deep_pink3')
                    console.print()
                    escriu_cartellera(mots)
                else:
                    text = Text.assemble(
                        ("Vaja! ", "red"), "No hi ha cap pel·lícula amb el nom del director que has escrit. Revisa haver-lo escrit correctament.")
                    console.print(text)
            else:
                console.print("Opció no vàlida", style="purple4")
        # mostrar el graf de busos.
        elif opcio == '3':
            try:
                console.print("Carregant la imatge del graf de busos...")
                show(g2)
                clear()
                console.print(
                    "Vols desar la imatge amb el mapa dels busos en un fitxer? ", end='')
                console.print("1. Sí", "2. No", end='\n', style='medium_purple2')
                n = input()
                if n == '1':
                    plot(g2, "graf_busos.png")
            except:
                console.print(
                    "Alguna cosa no ha funcionat com tocava. Torna-ho a intentar!")
        # mostrar el graf de ciutat.
        elif opcio == '4':
            try:
                console.print("Carregant la imatge del graf de la ciutat...")
                show(city)
                clear()
                console.print(
                    "Vols desar la imatge amb el mapa de la ciutat en un fitxer? ", end='', style='medium_purple2')
                console.print("1. Sí", "2. No", end='\n')
                n = input()
                if n == '1':
                    plot(city, "graf_barcelona.png")
            except:
                console.print(
                    "Alguna cosa no ha funcionat com tocava. Torna-ho a intentar!")
        # mostrar el camí per anar a veure una pel·lícula desitjada des d'un lloc donat en un moment donat. De totes les projeccions possibles cal mostrar el camí per arribar a la que comenci abans (i que s'hi pugui arribar a temps a peu i en bus).
        elif opcio == '5':
            geolocator = Nominatim(user_agent="geocoder_ap2")
            sessions = cartellera.cerca_pelicula()
            clear()
            if not len(sessions):
                text = Text.assemble(
                    ("Vaja! ", "red"), "La pel·lícula que has introduit no es troba a la cartellera. Consulta-la.")
                console.print(text)
                continue
            escriu_cartellera(list(sessions))
            console.print("Escriu a quin cinema vols anar.", style='medium_purple2')
            cine = input()
            sessions2 = combina(sessions, 2, cine)
            if not len(sessions2):
                text = Text.assemble(
                    ("Vaja! ", "red"), "No hi ha cap coincidència entre el cinema i pel·lícula que has escollit o potser no has escrit bé el nom del cinema. Revisa haver-lo escrit correctament.")
                console.print(text)
                continue
            clear()
            escriu_cartellera(list(sessions2))
            console.print(
                "Des de quina adreça de Barcelona vols sortir? És important que escriguis el tipus de via i el municipi.")
            adreça = input()
            try:
                coordenades: Coord = geolocator.geocode(adreça)
                if coordenades is not None:
                    clear()
                    console.print("Creant camí des de", adreça,
                                    "fins a", cinemes()[cine].address, style='medium_purple2')
                    lat, lon = coordenades.latitude, coordenades.longitude
                    if not coordenades_barcelona(lat, lon):
                        console.print(
                            "L'adreça que has introduit no es troba dins el municipi de Barcelona o no s'han pogut trobar les coordenades correctament. Prova-ho de nou afegint informació com el codi postal o el municipi. Disculpa!")
                        continue
                    cami = find_path(g1, city, (lon, lat),
                                        cinemes()[cine].coordenades)
                    t = total_time_path(cami)
                    console.print(
                        F"El temps de durada del recorregut és de {round(t/60)} minuts")

                    plot(cami, "cami_cinema.png")
                    s = input("Vols sortir ara? 1. Sí 2. No ")
                    if s == '1':
                        arriba = check_time(t//60, sessions2)
                        if arriba != -1:
                            hora = sessions2[arriba].time()
                            console.print(
                                f"Arribes a la sessió de les {hora[0]:02d}:{hora[1]:02d}! Gaudeix de la película!", style="bold chartreuse1")
                        else:
                            console.print(
                                "No arribes a cap sessió a hora! Cerca una altra pel·lícula o cinema a la cartellera.", style="deep_pink4")
                    elif s == '2':
                        console.print("A quina hora vols partir? Escriu només el nombre de l'hora. ", style='medium_purple2')
                        actual = input()
                        arriba = check_time(round(t/60), sessions2, actual)
                        if arriba != -1:
                            hora = sessions2[arriba].time()
                            console.print(
                                f"Arribes a la sessió de les {hora[0]:02d}:{hora[1]:02d}! Gaudeix de la película!",  style="bold chartreuse1")
                        else:
                            console.print(
                                "No arribes a cap sessió a hora! Cerca una altra pel·lícula o cinema a la cartellera.", style="deep_pink4")
                    else:
                        console.print("Opció no vàlida", style="purple4")
            except:
                text = Text.assemble(
                   ("Vaja! ", "red"), "Alguna cosa no ha anat bé. Torna a provar-ho.")
                console.print(text)
            else:
                text = Text.assemble(
                    ("Vaja! ", "red"), "El programa no és capaç de trobar coordenades per la teva adreça. Prova d'escriure-la més extensament, afegint codi postal o ciutat.")
                console.print(text)
        # crèdits
        elif opcio == '6':
            console.print("Aleix Albaiges Torres i Gabriel Fortuny Carretero", style="sandy brown")
        # sortir
        elif opcio == '7':
            break

        else:
            console.print("Opció no vàlida", style="purple4")

    console.print(
        "Adéu! Gràcies per visitar el nostre projecte. Aleix i Gabriel", style='magenta3')

def combina(sessions: list[Projection], y: int, cine: str = '') -> list[Projection]:
    """Donades les sessions ja condicionades per un paràmetre, se les redueix al segon paràmetre i es retorna una llista de projeccions que compleixen ambdues restriccions."""
    console = Console()
    # y agafa els valors: 1 -- Pel·licula, 2 -- Cinema, 3 -- Hora.
    if y == 1:
        console.print("Quina Pel·licula vols cercar? ", end='', style="light_pink3")
        pel = input()
        combinacio = [
            x for x in sessions if x.film().title in pel]
        return combinacio
    elif y == 2:
        if cine == '':
            console.print("A quin Cinema vols anar? ", end='', style="light_pink3")
            cine = input()
        combinacio = [
            x for x in sessions if x.cinema().name in cine]
        return combinacio
    elif y == 3:
        console.print(
            "A quina Hora vols anar al cine? Escriu l'hora en punt. ", end='', style="light_pink3")
        pel = yogi.read(int)
        combinacio = [x for x in sessions if x.time()[
            0] == pel]
        return combinacio
    else:
        console.print("Opció no vàlida", style="purple4")
        return list()

def coordenades_barcelona(lat: float, lon: float) -> bool:
    
    if lat <= 41.27:
        if lat >= 41.26 and 2.1 <= lon <= 2.12:
            return True
        elif lat >= 41.25 and 2.08 <= lon <= 2.13:
            return True
        elif lat >= 41.24 and 2.07 <= lon <= 2.13:
            return True
        elif lat >= 41.23 and 2.07 <= lon <= 2.12:
            return True
        elif lat >= 41.22 and 2.08 <= lon <= 2.11:
            return True
        elif lat >= 41.21 and 2.09 <= lon <= 2.10:
            return True
    return False

def escriu_cartellera(projeccions: list[Projection]) -> None:
    """Donada una llista de projeccions s'escriu en una taula del modul rich les sessions amb els elements: Titol, Cinema, Hora."""
    if len(projeccions):
        sort_hora(projeccions)
        console = Console()
        taula = Table(title="Cartellera de Barcelona")
        taula.add_column("Pel·lícula")
        taula.add_column("Cinema")
        taula.add_column("Hora")
        for projeccio in projeccions:
            taula.add_row(Text.assemble((projeccio.film().title, "medium_turquoise")), Text.assemble((projeccio.cinema(
            ).name, "aquamarine3")), Text.assemble((f"{projeccio.time()[0]:02d}:{projeccio.time()[1]:02d}", "sea_green2")))

    console.print(taula)


def check_time(time: int, sessions: list[Projection], actual: int = None) -> int:
    """Retorna la projeccio a la que s'arriba segons l'hora proporcionada."""
    
    if actual is None: # Si l'usuari vol sortir en el moment d'execució.
        temps_ara = datetime.now().time()
        actual = round(temps_ara.hour)
    hora = time // 60
    minuts = time % 60
    hora = int(hora)
    minuts = int(minuts)
    actual = int(actual)

    temps_donat = datetime(year=2023, month=5, day=26,
                           hour=hora+actual, minute=minuts, second=0, microsecond=0)
    for proj in range(len(sessions)):
        if temps_donat.hour < sessions[proj].time()[0]:
            return proj
        elif temps_donat.hour == sessions[proj].time()[0] and temps_donat.minute <= sessions[proj].time()[1]:
            return proj
    return -1 # En cas que no hi hagi projeccions.

def sort_hora(projections: list[Projection]) -> None:
    """Ordena la llista de projeccions projections per horari de petit a gran."""
    sorted(projections, key=lambda x: x.time()[0])

def clear():
    """Funciona com el clear a la terminal."""
    # Depèn del sistema operatiu de l'usuari.
    if os.name == "posix":  # Unix/Linux/MacOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")

# PASSAR LES FUNCIONS AL BILLBOARD - ok
# TREURE MAIN -- ok
# POSAR # -- ok
# COLORS --ok
# README i requirements
# pep8 -- pep8 — show-source —show-pep8 city.py 
# language -- ok
# limits coordenades --ok



if __name__ == '__main__':
    main()
