import yogi
from city import *
from billboard import *
from rich.console import Console
from rich.table import Table
from rich.text import Text
from geopy.geocoders import Nominatim
from datetime import datetime


def mostra() -> None:
    console = Console()
    clear()
    console.print("Benvingut!",
                  style="aquamarine1 bold", highlight=True)

    cartellera = read()  # S'inicialitzen la cartellera i els grafs al principi
    #  doncs així no s'han d'inicialitzar per cada cerca que es vulgui fer.
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
                       "5. Cerca per mot", "6. Genere", "7. Actor",
                       "8. Director"]
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
                    text = Text.assemble(("Vaja! ", "red"),
                                         ("La pel·lícula no es troba",
                                          "a la cartellera. ",
                                          "Assegura't que hi sigui o",
                                          "mira si l'has escrit bé.", "cyan"))
                    console.print(text)

                else:
                    clear()
                    film = sessions[0].film()
                    console.print("Projeccions de", film.title,
                                  style="yellow2")
                    console.print("Gèneres:", *film.genre,
                                  style="yellow2")
                    console.print("Actors i actrius:", *film.actors,
                                  style="yellow2")
                    console.print("Director/s:", *film.director,
                                  style="yellow2")
                    console.print()
                    escriu_cartellera(sessions)

            elif cerca == '2':
                sessions = cartellera.cerca_cinema()
                if not len(sessions):
                    text = Text.assemble(("Vaja! ", "red"), "El cinema que",
                                         "no es troba a la cartellera. ",
                                         ("Assegura't que hi sigui",
                                          "o mira si l'has escrit bé.",
                                          "cyan"))
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
                        ("Vaja! ", "red"), "No hi ha cap pel·lícula",
                        "programada",
                        "per aquesta hora o no l'has escrit correctament.")
                    console.print(text)
                else:
                    clear()
                    hora = sessions[0].time()
                    console.print("Projeccions a les",
                                  f"{hora[0]:02d}:{hora[1]:02d}",
                                  style="yellow2")
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
                    "Escull els dos paràmetres amb els que vols cercar. ",
                    end='')
                try:
                    x, y = yogi.read(int), yogi.read(int)
                    clear()
                    if x == 1:
                        sessions = cartellera.cerca_pelicula()
                        combinacio = combina(sessions, y)
                        film = combinacio[0].film()
                        if len(combinacio):
                            console.print("Projeccions de", film.title,
                                          style="yellow2")
                            console.print("Gèneres:", *film.genre,
                                          style="yellow2")
                            console.print("Actors i actrius:", *film.actors,
                                          style="yellow2")
                            console.print("Director/s:", *film.director,
                                          style="yellow2")
                            console.print()

                    elif x == 2:
                        sessions = cartellera.cerca_cinema()
                        combinacio = combina(sessions, y)
                        if len(combinacio):
                            c = combinacio[0].cinema()
                            console.print("Projeccions a", c.name,
                                          style="yellow2")
                            console.print(
                                "Adreça:", c.address, style="yellow2")
                            console.print()

                    elif x == 3:
                        sessions = cartellera.cerca_horari()
                        combinacio = combina(sessions, y)
                        if len(combinacio):
                            hora = combinacio[0].time()
                            console.print("Projeccions a les",
                                          f"{hora[0]:02d}:{hora[1]:02d}",
                                          style="yellow2")
                            console.print()

                    else:
                        console.print("Opció no vàlida", style="purple4")
                    if len(combinacio):
                        escriu_cartellera(combinacio)
                    else:
                        text = Text.assemble(
                            ("Vaja! ", "red"),
                            "No hi ha cap combinació amb els paràmetres",
                            "donats.")
                        console.print(text)
                except Exception:
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
                        ("Vaja! ", "red"),
                        "No hi ha cap pel·lícula o cinema amb el mot escrit.")
                    console.print(text)
            elif cerca == '6':
                taula = Table()
                generes = ['Acción', 'Animación', 'Aventura', 'Biografía',
                           'Ciencia ficción', 'Comedia', 'Comedia dramática',
                           'Comedia musical', 'Crimen', 'Documental', 'Drama',
                           'Familia', 'Fantasía', 'Guerra', 'Histórico',
                           'Judicial', 'Musical', 'Romántico', 'Suspense',
                           'Terror', 'Western']
                taula.add_column("Gèneres")
                for genre in generes:
                    taula.add_row(genre, style='medium_purple2')
                console.print(taula)
                console.print(
                    "Quin gènere vols cercar? Escrit en castellà. ", end='',
                    style='medium_purple2')
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
                        ("Vaja! ", "red"),
                        "No hi ha cap pel·lícula amb el gènere escrit o no",
                        "s'ha escrit correctament.")
                    console.print(text)
            elif cerca == '7':
                console.print("Quin actor vols cercar? ", end='',
                              style='medium_purple2')
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
                        ("Vaja! ", "red"),
                        "No hi ha cap pel·lícula amb el nom",
                        "de l'actor que has escrit. Revisa haver-lo",
                        "escrit correctament.")
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
                        ("Vaja! ", "red"),
                        "No hi ha cap pel·lícula amb el nom",
                        "del director que has escrit. Revisa haver-lo",
                        "escrit correctament.")
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
                    "Vols desar la imatge amb el mapa dels busos en un",
                    "fitxer? ", end='')
                console.print("1. Sí", "2. No", end='\n',
                              style='medium_purple2')
                n = input()
                if n == '1':
                    plot(g2, "graf_busos.png")
            except Exception:
                console.print(
                    "Alguna cosa no ha funcionat com tocava. Torna-ho a",
                    "intentar!")
        # mostrar el graf de ciutat.
        elif opcio == '4':
            try:
                console.print("Carregant la imatge del graf de la ciutat...")
                show(city)
                clear()
                console.print(
                    "Vols desar la imatge amb el mapa de la ciutat en un",
                    "fitxer? ", end='', style='medium_purple2')
                console.print("1. Sí", "2. No", end='\n')
                n = input()
                if n == '1':
                    plot(city, "graf_barcelona.png")
            except Exception:
                console.print(
                    "Alguna cosa no ha funcionat com tocava. Torna-ho a",
                    "intentar!")
        # Mostrar el camí per anar a veure una pel·lícula desitjada des d'un
        # lloc donat en un moment donat. De totes les projeccions possibles
        # cal mostrar el
        # camí per arribar a la que comenci abans (i que s'hi pugui
        # arribar a temps a peu
        # i en bus).
        elif opcio == '5':
            geolocator = Nominatim(user_agent="geocoder_ap2")
            sessions = cartellera.cerca_pelicula()
            clear()
            if not len(sessions):
                text = Text.assemble(
                    ("Vaja! ", "red"),
                    "La pel·lícula que has introduit no es troba a la",
                    "cartellera. Consulta-la.")
                console.print(text)
                continue
            escriu_cartellera(list(sessions))
            console.print("Escriu a quin cinema vols anar.",
                          style='medium_purple2')
            cine = input()
            sessions2 = combina(sessions, 2, cine)
            if not len(sessions2):
                text = Text.assemble(
                    ("Vaja! ", "red"), "No hi ha cap coincidència entre el",
                    "cinema i pel·lícula que has escollit o potser no has",
                    "escrit bé el nom del cinema.",
                    "Revisa haver-lo escrit correctament.")
                console.print(text)
                continue
            clear()
            escriu_cartellera(list(sessions2))
            console.print(
                "Des de quina adreça de Barcelona vols sortir? És important "
                "que escriguis el tipus de via i el municipi.")
            adreça = input()
            try:
                coordenades: Coord = geolocator.geocode(adreça)
                if coordenades is not None:
                    clear()
                    console.print("Creant camí des de", adreça,
                                  "fins a", cinemes()[cine].address,
                                  style='medium_purple2')
                    lat, lon = coordenades.latitude, coordenades.longitude
                    if not coordenades_barcelona(lat, lon):
                        console.print(
                            "L'adreça que has introduit no es troba dins el",
                            "municipi de Barcelona o no s'han pogut trobar",
                            "les coordenades correctament.",
                            "Prova-ho de nou afegint informació com el codi",
                            "postal o el municipi. Disculpa!")
                        continue
                    cami = find_path(g1, city, (lon, lat),
                                     cinemes()[cine].coordenades)
                    t = total_time_path(cami)
                    console.print(
                        F"El temps de durada del recorregut és",
                        F"de {round(t/60)} minuts")

                    plot(cami, "cami_cinema.png")
                    s = input("Vols sortir ara? 1. Sí 2. No ")
                    if s == '1':
                        arriba = mira_temps(t//60, sessions2)
                        if arriba != -1:
                            hora = sessions2[arriba].time()
                            console.print(
                                f"Arribes a la sessió de les",
                                F"{hora[0]:02d}:{hora[1]:02d}!",
                                "Gaudeix de la pel·lícula!",
                                style="bold chartreuse1")
                        else:
                            console.print(
                                "No arribes a cap sessió a hora! Cerca una",
                                "altra pel·lícula o cinema a la cartellera.",
                                style="deep_pink4")
                    elif s == '2':
                        console.print("A quina hora vols partir? Escriu hora",
                                      "i minut separats.",
                                      style='medium_purple2')
                        try:
                            actual = yogi.read(int)
                            min_actual = yogi.read(int)
                        except Exception:
                            console.print("Format d'hora incorrecte.")
                        arriba = mira_temps(round(t/60), sessions2, actual,
                                            min_actual)
                        if arriba != -1:
                            hora = sessions2[arriba].time()
                            console.print(
                                f"Arribes a la sessió de les",
                                F"{hora[0]:02d}:{hora[1]:02d}!",
                                "Gaudeix de la pel·lícula!",
                                style="bold chartreuse1")
                        else:
                            console.print(
                                "No arribes a cap sessió a hora! Cerca una",
                                "altra pel·lícula o cinema a la cartellera.",
                                style="deep_pink4")
                    else:
                        console.print("Opció no vàlida", style="purple4")
                else:
                    text = Text.assemble(
                        ("Vaja! ", "red"),
                        "El programa no és capaç de trobar coordenades ",
                        "per la teva ",
                        "adreça. Prova d'escriure-la més extensament, afegint",
                        " codi postal o municipi.")
                    console.print(text)
            except Exception:
                text = Text.assemble(
                    ("Vaja! ", "red"),
                    "Alguna cosa no ha anat bé. Torna a provar-ho.")
                console.print(text)
        # crèdits
        elif opcio == '6':
            console.print("Aleix Albaiges Torres i Gabriel Fortuny Carretero",
                          style="sandy_brown")
            console.print("Tria pel·lícula i ves-hi en bus! Aquest",
                          "és un projecte de l'assignatura d'Algorísmia i",
                          "Programació 2 del Grau en Ciència i Enginyeria",
                          "de Dades de la UPC.",
                          style="sea_green3")
            console.print("Es tracta d'un programa",
                          "dinàmic,",
                          "en el què pots navegar. Escull i cerca una",
                          "pel·lícula, mira't",
                          "quines sessions té i et direm com anar-hi",
                          "el més ràpid",
                          "possible.",
                          style="sea_green3")
            console.print("Tens moltes maneres de cercar el",
                          "contingut i es",
                          "mostren grafs amb mapes sobreimpressionats.",
                          "Gaudeix!",
                          style="sea_green3")
        # sortir
        elif opcio == '7':
            break

        else:
            console.print("Opció no vàlida", style="purple4")

    console.print(
        "Adéu! Gràcies per visitar el nostre projecte. Aleix i Gabriel",
        style='magenta3')


def combina(sessions: list[Projection], y: int,
            cine: str = '') -> list[Projection]:
    """Donades les sessions ja condicionades per un paràmetre, se les redueix
    al segon paràmetre i es retorna una llista de projeccions que compleixen
    ambdues restriccions."""
    console = Console()
    # y agafa els valors: 1 -- Pel·licula, 2 -- Cinema, 3 -- Hora.
    if y == 1:
        console.print("Quina Pel·licula vols cercar? ", end='',
                      style="light_pink3")
        pel = input()
        combinacio = [
            x for x in sessions if x.film().title in pel]
        return combinacio
    elif y == 2:
        if cine == '':
            console.print("A quin Cinema vols anar? ",
                          end='', style="light_pink3")
            cine = input()
        combinacio = [
            x for x in sessions if x.cinema().name in cine]
        return combinacio
    elif y == 3:
        console.print(
            "A quina Hora vols anar al cine? Escriu l'hora en punt. ",
            end='', style="light_pink3")
        pel = yogi.read(int)
        combinacio = [x for x in sessions if x.time()[
            0] == pel]
        return combinacio
    else:
        console.print("Opció no vàlida", style="purple4")
        return list()


def coordenades_barcelona(lat: float, lon: float) -> bool:
    """Limita les coordenades i retorna si es troben dins
    el municipi de Barcelona."""
    if lat <= 41.45:
        if lat >= 41.43 and 2.17 <= lon <= 2.25:
            return True
        elif lat >= 41.42 and 2.13 <= lon <= 2.23:
            return True
        elif lat >= 41.4 and 2.11 <= lon <= 2.22:
            return True
        elif lat >= 41.38 and 2.11 <= lon <= 2.2:
            return True
        elif lat >= 41.37 and 2.13 <= lon <= 2.18:
            return True
        elif lat >= 41.35 and 2.15 <= lon <= 2.17:
            return True
    return False


def escriu_cartellera(projeccions: list[Projection]) -> None:
    """Donada una llista de projeccions s'escriu en una taula
    del modul rich les sessions amb els elements: Titol,
    Cinema, Hora."""
    if len(projeccions):
        sort_hora(projeccions)
        console = Console()
        taula = Table(title="Cartellera de Barcelona")
        taula.add_column("Pel·lícula")
        taula.add_column("Cinema")
        taula.add_column("Hora")
        for projeccio in projeccions:
            t = projeccio.time()
            taula.add_row(Text.assemble((projeccio.film().title,
                                         "medium_turquoise")),
                          Text.assemble((projeccio.cinema(
                          ).name, "aquamarine3")),
                          Text.assemble((f"{t[0]:02d}:{t[1]:02d}",
                                         "sea_green2")))

    console.print(taula)


def mira_temps(time: int, sessions: list[Projection],
               actual: int = None, min_actual: int = 0) -> int:
    """Retorna la projeccio a la que s'arriba segons l'hora proporcionada."""

    if actual is None:  # Si l'usuari vol sortir en el moment d'execució.
        temps_ara = datetime.now().time()
        actual = round(temps_ara.hour)
        min_actual = round(temps_ara.minute)

    hora = time // 60
    minuts = time % 60
    hora = int(hora)
    minuts = int(minuts)
    actual = int(actual)
    min_actual = int(min_actual)
    temps_donat = datetime(year=2023, month=5, day=26,
                           hour=hora+actual, minute=minuts+min_actual,
                           second=0,
                           microsecond=0)
    for proj in range(len(sessions)):
        s = sessions[proj].time()
        t = temps_donat
        if t.hour < s[0]:
            return proj
        elif t.hour == s[0] and t.minute <= s[1]:
            return proj
    return -1    # En cas que no hi hagi projeccions.


def sort_hora(projections: list[Projection]) -> None:
    """Ordena la llista de projeccions projections per horari
    de petit a gran."""
    sorted(projections, key=lambda x: x.time()[0])


def clear():
    """Funciona com el clear a la terminal."""
    # Depèn del sistema operatiu de l'usuari.
    if os.name == "posix":  # Unix/Linux/MacOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")


if __name__ == '__main__':
    mostra()
