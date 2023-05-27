import yogi
from city import *
from billboard import *
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table


def main() -> None:
    # mostrar el nom dels autors del projecte.
    console = Console()
    console.print("Aleix Albaiges i Gabriel Fortuny", style="bold")
    
    cartellera = read()
    
    instruccions = [
        "1. Crea la cartellera",
    "2. Mostra el contingut de la cartellera",
    "3. Cerca a la cartellera",
    "4. Crea el graf de busos",
    "5. Mostra el graf de busos",
    "6. Crea el graf de ciutat",
    "7. Mostra el graf de ciutat,"
    "8. Mostra el camí per anar a veure una pel·lícula",
    "9. Sortir"
    ]
    
    while True:
        for inst in instruccions: console.print(inst)
        console.print("Selecciona una opció:", end='')
        opcio = yogi.read(int)
        
        if opcio == 1:
            taula = Table(title="Cartellera de Barcelona")
            taula.add_column("Pel·lícula")
            taula.add_column("Cinema")
            taula.add_column("Hora")
            
            for projeccio in cartellera.projections():
                taula.add_row(projeccio.film().title, projeccio.cinema().name, str(projeccio.time()[0])+':'+str(projeccio.time()[1]))
                
            console.print(taula)
    # crear la cartellera.
    # mostrar el contingut de la cartellera.
    # cercar a la cartellera.
    # crear el graf de busos.
    # mostrar el graf de busos.
    # crear el graf de ciutat.
    # mostrar el graf de ciutat.
    # mostrar el camí per anar a veure una pel·lícula desitjada des d'un lloc donat en un moment donat. De totes les projeccions possibles cal mostrar el camí per arribar a la que comenci abans (i que s'hi pugui arribar a temps a peu i en bús).




if __name__ == '__main__':
    main()
