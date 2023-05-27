import yogi
from city import *
from billboard import *
from rich.console import Console
from rich.table import Table
from rich.text import Text


def main() -> None:
    # mostrar el nom dels autors del projecte.
    console = Console()
    console.print("Aleix Albaiges i Gabriel Fortuny", style="bold")

    cartellera = read()
    busos = get_buses_graph()
    ciutat = ...  # no sé
    instruccions = [
        "1. Mostra el contingut de la cartellera",
        "2. Cerca a la cartellera",
        "3. Mostra el graf de busos",
        "4. Mostra el graf de ciutat",
        "5. Mostra el camí per anar a veure una pel·lícula",
        "6. Sortir"
    ]

    while True:
        for inst in instruccions:
            console.print(inst)
        console.print("Selecciona una opció: ", end='')
        opcio = yogi.read(int)
        # mostrar el contingut de la cartellera.
        if opcio == 1:
            escriu_cartellera(cartellera.projections())
        # cercar a la cartellera.
        elif opcio == 2:
            cerques = ["1. Pel·lícula", "2. Cinema", "3. Horari", "4. Combina"]
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
                    escriu_cartellera(list(sessions))

            elif cerca == 2:
                sessions = cerca_cinema(cartellera)
                if not len(sessions):
                    text = Text.assemble(("Vaja! ", "red"), "El cinema que has introduit no es troba a la cartellera. ",  (
                        "Assegura't d'escriure'n un que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                    console.print(text)
                else:
                    escriu_cartellera(list(sessions))

            elif cerca == 3:
                sessions = cerca_horari(cartellera)
                if len(sessions) == 0:
                    text = Text.assemble(
                        ("Vaja! ", "red"), "No hi ha cap pel·lícula programada per aquesta hora o no l'has escrit correctament.")
                    console.print(text)
                else:
                    escriu_cartellera(list(sessions))

            elif cerca == 4:
                combos = ["1. Pel·lícula", "2. Cinema", "3. Horari"]
                for combo in combos:
                    console.print(combo)
                console.print(
                    "Escull els dos paràmetres amb els que vols cercar.", end='')
                x, y = yogi.read(int), yogi.read(int)

                if x == 1:
                    sessions = cerca_pelicula(cartellera)
                    if y == 2:
                        console.print("A quin Cinema vols anar? ", end='')
                        cine = input()
                        combinacio = {
                            x for x in sessions if x.cinema().name == cine}
                        escriu_cartellera(list(combinacio))
                    elif y == 3:
                        console.print(
                            "A quina Hora vols anar al cine? Escriu l'hora en punt. ", end='')
                        pel = yogi.read(int)
                        combinacio = {x for x in sessions if x.time()[
                            0] == pel}
                        escriu_cartellera(list(combinacio))
                    else:
                        console.print("Opció no vàlida", style="purple4")

                elif x == 2:
                    sessions = cerca_cinema(cartellera)
                    if y == 1:
                        console.print("Quina Pel·licula vols cercar? ", end='')
                        pel = input()
                        combinacio = {
                            x for x in sessions if x.film().title == pel}
                        escriu_cartellera(list(combinacio))
                    elif y == 3:
                        console.print(
                            "A quina Hora vols anar al cine? Escriu l'hora en punt. ", end='')
                        pel = yogi.read(int)
                        combinacio = {x for x in sessions if x.time()[
                            0] == pel}
                        escriu_cartellera(list(combinacio))
                    else:
                        console.print("Opció no vàlida", style="purple4")
                elif x == 3:
                    sessions = cerca_horari(cartellera)
                    if y == 1:
                        console.print("Quina Pel·licula vols cercar? ", end='')
                        pel = input()
                        combinacio = {
                            x for x in sessions if x.film().title == pel}
                        escriu_cartellera(list(combinacio))
                    elif y == 2:
                        console.print("A quin Cinema vols anar? ", end='')
                        cine = input()
                        combinacio = {
                            x for x in sessions if x.cinema().name == cine}
                        escriu_cartellera(list(combinacio))
                    else:
                        console.print("Opció no vàlida", style="purple4")
                else:
                    console.print("Opció no vàlida", style="purple4")
            else:
                console.print("Opció no vàlida", style="purple4")
        # mostrar el graf de busos.
        elif opcio == 3:
            show(busos)
        # mostrar el graf de ciutat.
        elif opcio == 4:
            show()
        # # mostrar el camí per anar a veure una pel·lícula desitjada des d'un lloc donat en un moment donat. De totes les projeccions possibles cal mostrar el camí per arribar a la que comenci abans (i que s'hi pugui arribar a temps a peu i en bús).
        elif opcio == 5:
            console.print(
                "Quina Pel·lícula vols veure? Si encara no ho saps consulta primer la cartellera.")
            pel = input()
            trobada = False
            for intent in cartellera.films():
                if intent.title == pel:
                    trobada = True
                    sessions = {x for x in cartellera.projections()
                                if pel == x.film().title}
                    escriu_cartellera(list(sessions))

            if not trobada:
                text = Text.assemble(("Vaja! ", "red"), "La pel·lícula que has introduit no es troba a la cartellera. ",  (
                    "Assegura't d'escriure una que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                console.print(text)

            # A partir d'aquí, calcula el cinema que estigui més a prop d'entre tots els que la fan en el temps possible per arribar-hi.
        elif opcio == 6:
            break

        elif opcio == 7:
            for projec in cartellera.projections():
                projec.escriu()

        else:
            console.print("Opció no vàlida", style="purple4")
        # crear la cartellera.
    console.print("Adeu! La consola s'ha tancat.", style='magenta3')

    # crear el graf de busos.

    # crear el graf de ciutat.
    #


def cerca_horari(cartellera: Billboard) -> set[Projection]:
    console = Console()
    console.print(
        "A quina Hora vols anar al cine? Escriu l'hora en punt. ", end='')
    pel = yogi.read(int)

    sessions = {x for x in cartellera.projections() if pel == x.time()[0]}
    return sessions


def cerca_pelicula(cartellera: Billboard) -> set[Projection]:
    console = Console()
    console.print("Quina Pel·licula vols cercar? ", end='')
    pel = input()

    sessions: set[Projection] = set()
    sessions = {x for x in cartellera.projections() if pel == x.film().title}
    return sessions


def cerca_cinema(cartellera: Billboard) -> set[Projection]:
    console = Console()
    console.print("A quin Cinema vols anar? ", end='')
    cine = input()

    sessions: set[Projection] = set()
    sessions = {x for x in cartellera.projections() if cine == x.cinema().name}

    return sessions


def escriu_cartellera(projeccions: list[Projection]) -> None:
    console = Console()
    taula = Table(title="Cartellera de Barcelona")
    taula.add_column("Pel·lícula")
    taula.add_column("Cinema")
    taula.add_column("Hora")
    repetits: dict[str, dict[str, set[tuple[int, int]]]] = dict()
    for projeccio in projeccions:
        try:
            if projeccio.time() in repetits[projeccio.film().title][projeccio.cinema().name]:
                continue
        except KeyError:
            taula.add_row(projeccio.film().title, projeccio.cinema(
            ).name, f"{projeccio.time()[0]:02d}:{projeccio.time()[1]:02d}")
            repetits[projeccio.film().title] = {projeccio.cinema().name: set()}
            repetits[projeccio.film().title][projeccio.cinema().name].add(
                projeccio.time())
    console.print(taula)


if __name__ == '__main__':
    main()
