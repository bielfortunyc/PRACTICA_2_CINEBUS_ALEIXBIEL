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
    ciutat = show()
    instruccions = [
        "1. Mostra el contingut de la cartellera",
    "2. Cerca a la cartellera",
    "3. Mostra el graf de busos",
    "4. Mostra el graf de ciutat",
    "5. Mostra el camí per anar a veure una pel·lícula",
    "6. Sortir"
    ]
    
    while True:
        for inst in instruccions: console.print(inst)
        console.print("Selecciona una opció: ", end='')
        opcio = yogi.read(int)
        # mostrar el contingut de la cartellera.
        if opcio == 1:
            escriu_cartellera(cartellera.projections())                
        # cercar a la cartellera.   
        elif opcio == 2:
            cerques = ["1. Pel·lícula", "2. Cinema", "3. Horari"]
            for cerca in cerques: console.print(cerca)
            console.print("Què vols cercar? ", end='')
            cerca = yogi.read(int)
            if cerca == 1:
                console.print("Quina Pel·licula vols cercar? ", end='')
                pel = input()
                trobada = False
                for intent in cartellera.films():
                    if intent.title == pel:
                        trobada = True
                        sessions = {x for x in cartellera.projections() if pel == x.film().title}
                        escriu_cartellera(list(sessions))
                        
                if not trobada: 
                    text = Text.assemble(("Vaja! ", "red"), "La pel·lícula que has introduit no es troba a la cartellera. ",  ("Assegura't d'escriure una que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                    console.print(text)
            elif cerca == 2:
                console.print("A quin Cinema vols anar? ", end='')
                cine = input()
                trobada = False
                for intent in cartellera.cinemes():
                    if intent.name == cine:
                        trobada = True
                        sessions = {x for x in cartellera.projections() if cine == x.cinema().name}
                        escriu_cartellera(list(sessions))
                        
                if not trobada: 
                    text = Text.assemble(("Vaja! ", "red"), "El cinema que has introduit no es troba a la cartellera. ",  ("Assegura't d'escriure'n un que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                    console.print(text)
            elif cerca == 3:
                console.print("A quina Hora vols anar al cine? Escriu l'hora en punt. ", end='')
                pel = yogi.read(int)
                trobada = False
                for intent in cartellera.projections():
                    if intent.time()[0] == pel:
                        trobada = True
                        sessions = {x for x in cartellera.projections() if pel == x.time()[0]}
                        escriu_cartellera(list(sessions))
                        
                if not trobada: 
                    text = Text.assemble(("Vaja! ", "red"), "No hi ha cap pel·lícula programada per aquesta hora o no l'has escrit correctament.")
                    console.print(text)
            else: console.print("Opció no vàlida", style="purple4")
        # mostrar el graf de busos.
        elif opcio == 3:
            show(busos)
        # mostrar el graf de ciutat.
        elif opcio == 4:
            show()
        # # mostrar el camí per anar a veure una pel·lícula desitjada des d'un lloc donat en un moment donat. De totes les projeccions possibles cal mostrar el camí per arribar a la que comenci abans (i que s'hi pugui arribar a temps a peu i en bús).
        elif opcio == 5:
            console.print("Quina Pel·lícula vols veure? Si encara no ho saps consulta primer la cartellera.")
            pel = input()
            trobada = False
            for intent in cartellera.films():
                if intent.title == pel:
                    trobada = True
                    sessions = {x for x in cartellera.projections() if pel == x.film().title}
                    escriu_cartellera(list(sessions))
                    
            if not trobada: 
                text = Text.assemble(("Vaja! ", "red"), "La pel·lícula que has introduit no es troba a la cartellera. ",  ("Assegura't d'escriure una que hi sigui o fixa't en si l'has escrit bé.", "cyan"))
                console.print(text)
            
            # A partir d'aquí, calcula el cinema que estigui més a prop d'entre tots els que la fan en el temps possible per arribar-hi.
                        
        else: console.print("Opció no vàlida", style="purple4")
        # crear la cartellera.
    
    
    # crear el graf de busos.
    
    # crear el graf de ciutat.
    #
    


def escriu_cartellera(projeccions: list[Projection]) -> None:
    console = Console()
    taula = Table(title="Cartellera de Barcelona")
    taula.add_column("Pel·lícula")
    taula.add_column("Cinema")
    taula.add_column("Hora")
    
    for projeccio in projeccions:
        taula.add_row(projeccio.film().title, projeccio.cinema().name, f"{projeccio.time()[0]:02d}:{projeccio.time()[1]:02d}")

    console.print(taula)

if __name__ == '__main__':
    main()
