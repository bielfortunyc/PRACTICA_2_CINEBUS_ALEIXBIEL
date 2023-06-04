# CineBus Aleix Albaiges i Gabriel Fortuny.

## Introducció
Segona pràctica d'Algorísmia i Programació del Grau en Ciència i Enginyeria de Dades del curs 2022-23.
Alumnes: Aleix Albaiges Torres i Gabriel Fortuny Carretero.
Llenguatge dde programació: Python.
Nom de la pràctica: CineBus.

### Prerequisits

Les llibreries necessàries per executar el projecte estan escrites al requirements.txt.
Per executar requirements:

python -m pip install -r requirements.txt

Aquests inclouen les següents llibreries:
dataclasses, re, json, bs4, requests, typing, networkx, urllib.request, staticmap, os, matplotlib.pyplot, pickle, yogi i rich.
A més, és necessari una versió de Python que les tingui actualitzades. Mínim Python3.10.
També és important tenir espai de memòria a l'ordinador.

### Mòdul billboard
El mòdul billboard duu a terme totes les funcions per descarregar la informació de la web de Sensacine i convertir-la en projeccions. 

Consta de les classes Film, Cinema, Projection i Billboard, necessàries per dur a terme el projecte i de fàcil enteniment.

La classe Billboard és la més important, doncs conté tots els filtres de cerca per poder trobar les pel·lícules i cinemes desitjats.

La funció read() és la principal en aquest codi. S'encarrega de cridar les altres funcions i fa el paper, d'alguna manera, de main. El web_scraping es realitza a partir de les tres pàgines web de Sensacine de cinemes de Barcelona. Llavors les funcions que comencen per llista s'encarreguen de recórrer el fitxer html de item_resa enviat i amb els mòduls re i json extreure la informació important.

Finalment, la funció cinemes() conté un diccionari amb tots els cinemes disponibles de Barcelona, la seva adreça i coordenades. Ho hem fet així per tenir un accés més ràpid, doncs la llista de cinemes no varia en el temps, i per evitar dependre del mòdul geopy, doncs aquest pot donar molts errors quan no troba les adreces. És una manera d'assegurar-se que el més bàsic del projecte funcionarà correctament.

### Mòdul buses
El mòdul buses té com a objectiu crear un graf de les línies de bus a partir d'un fitxer JSON proporcionat per l'Agència de Mobilitat de Barcelona.

La funció get_buses_graph() és responsable de llegir les dades JSON des d'una URL específica, processar-les i construir el graf de les línies de bus. 

Aquesta funció comença llegint les dades JSON des de l'URL especificada utilitzant la llibreria urllib. Les dades són emmagatzemades en la variable data.
Tot seguit, es crea una instància buida del graf de línies de bus utilitzant nx.Graph() i s'emmagatzema en la variable graph.
La funció recorre les línies de bus i les seves parades a les dades JSON. Per a cada parada que pertanyi a la ciutat de Barcelona, s'extreuen les dades rellevants com l'identificador de la parada, les coordenades de longitud i latitud i el seu tipus, i s'afegeix un node al graf amb aquestes dades com atributs.

A continuació, la funció recorre les línies de bus i les seves parades per crear les arestes del graf. Si les parades d'origen i destí pertanyen a la ciutat de Barcelona, s'extreuen els identificadors de les parades i s'afegeix una aresta al graf amb l'atribut tipus.

Finalment, es retorna el graf de les línies de bus complet.

Finalment, té les funcions per mostrar el graf de manera interactivament per pantalla o com a fitxer .png.

### Mòdul city
El mòdul city és l'encarregat d'obtenir un graf de la ciutat de Barcelona conjuntament amb el graf de les línies de bus, i també de trobar el camí més curt per anar d'unes coordenades a unes altres. A més, conté les funcions per mostrar grafs per pantalla i per crear un fitxer .png del graf.

Per obtenir el graf de la ciutat de Barcelona, es fa amb la llibreria osmnx, com aquest procés triga bastant, el primer cop que es carrega el graf es guarda en el directori actual de l'usuari i si es vol tornar a accedir al graf es carrega el graf guardat prèviament.
Després es crea el graf fusió del graf de la ciutat de Barcelona amb el graf de les línies de bus, en aquest graf cada node tindrà com a atribut el seu identificador, les seves coordenades i el seu tipus, que servirà per diferenciar parades i cruïlles, les arestes tenen l'identificador del seu node origen i l'dentificador del seu node destí, a més del pes de l'aresta que en aquest cas és el temps que es triga a recorre-la i per últim el tipus, per diferenciar entre línies de bus i carrers.

També conté la funció per calcular el camí més curt per anar d'un punt a un altre, això servirà per saber quina és la manera més ràpida d'anar fins al cinema al qual es vulgui anar. 

Finalment, al igual que el mòdul buses té les funcions per mostrar interactivament el graf, que aquesta funció és igual i per crear el fitxer .png del graf del graf fusionat amb l'única diferència que en aquest cas fa distinció de colors ja que hi ha més d'un tipus de node i aresta.

### Mòdul demo
El mòdul demo ensambla el projecte i s'encarrega de mostrar-lo de manera intuitiva i dinàmica. Hem emprat el mòdul rich de python, doncs permet mostrar una terminal amb colors i text de manera estètica. A més, importa els altres codis: city i billboard.

Comença amb una funció mostra on es desenvolupa tota la projecció del projecte. Es donen les opcions que es poden dur a terme i de manera senzilla, escrivint el nombre, es pot navegar per dins el programa. La manera d'escriure a la terminal és senzilla i s'empra sobretot la funció input, doncs els noms de pel·lícules i cinemes són llargs.

Per fer cerques a la cartellera s'empren els mètodes de la classe Billboard. També es poden combinar cerques; la funció combina condiciona la cerca a dos paràmetres donats. La funció escriu_cartellera() mostra una taula amb la informació de cada projecció a partir d'una llista que ve donada amb les restriccions oportunes. Mostra nom de la pel·lícula, cinema i hora de començament. Amb la funció sort_hora() ens assegurem que les projeccions surten en ordre d'hora ascendent.

També s'ha fet una funció mira_temps() que retorna a quina de les projeccions possibles s'arriba a partir de l'hora donada. Aquesta pot ser el mateix moment en què s'executa el programa o pot ser la que l'usuari escrigui. En cas que no es pugui arribar a cap també n'avisa.

A més a més, la funció coordenades_barcelona() limita l'àrea geogràfica de Barcelona a les longituds i latituds adients. Per això retorna un booleà: cert si les coordenades donades es troben dins el municipal i fals altrament. És una bona aproximació, doncs el geopy no és massa precís i a vegades s'equivoca.

Finalment, s'ha de comentar que l'opció de mostrar el camí per anar al cine des de qualsevol adreça de Barcelona depèn en gran part pel mòdul geopy de Python. Aquest no troba algunes adreces i algunes les fa malament. El programa funciona bé quan les coordenades són correctes, però dibuixa un camí fals quan no ho són.

## Autors

* **Aleix Albaiges Torres** 
* **Gabriel Fortuny Carretero** 

## Llicència

Els autors del projecte ens reservem tots els drets i l'autoria d'aquest.

A més, la informació per la cartellera és agafada de la pàgina Sensacine, que és privada. Per això, aquest projecte no pot ser fer-se públic.

## Coneixements adquirits

* Hem après a emprar totes les llibreries de grafs i de web scraping, les quals eren totalment noves i desconegudes per nosaltres.
* Hem trobat solucions a problemes de codi que no ens havien aparegut fins ara.
* Hem creat una interfície a la terminal amb el mòdul rich per primera vegada.
* Hem fet un programa emprant bases de dades grans i creat grafs amb elles.
* Hem aplicat unes regles d'estil (pep8) estrictes i uniformes en tot el codi.
