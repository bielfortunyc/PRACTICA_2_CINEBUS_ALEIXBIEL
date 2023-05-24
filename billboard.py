from dataclasses import dataclass
import re
import json
from bs4 import BeautifulSoup
import requests
from typing import Any

@dataclass
class Film:
    title: str
    genre: str
    director: str
    actors: list[str]

    def __init__(
            self,
            elements: dict[str, Any]) -> None:
        self.title = elements['title']
        self.genre = elements['genre']
        self.director = elements['directors']
        self.actors = elements['actors']

    def escriu(self) -> None:
        print(
            'PEL LICULA: Titol:',
            self.title,
            'Genere:',
            self.genre,
            'Director/s:',
            self.director,
            'Actors:',
            self.actors)

class Cinema:
    name: str
    address: str
    coordenades : tuple[float,float] # Latitud, longitud

    def __init__(self, name: str, address: str, coordenades: tuple[float,float]) -> None:
        self.name = name
        self.address = address
        self.coordenades = coordenades
        
    def escriu(self) -> None:
        print(
            'CINEMA: Nom:',
            self.name,
            'Adreça:',
            self.address,
            'Coordenades:',
            self.coordenades[0], self.coordenades[1])
        
class Projection:
    _film: Film
    _cinema: Cinema
    _time: tuple[int, int]   # hora:minut
    #language: str de moment suda perquè no hi és a la info de Sensacine.

    def __init__(self, film: Film, cinema: Cinema,
                 time: tuple[int, int]) -> None:
        self._film, self._cinema, self._time = film, cinema, time

    def film(self) -> Film:
        return self._film

    def cinema(self) -> Cinema:
        return self._cinema

    def time(self) -> tuple[int, int]:
        return self._time

    def escriu(self) -> None:
        print(
            'PEL LICULA: Titol:',
            self.film().title,
            'Genere:',
            self.film().genre,
            'Director/s:',
            self.film().director,
            'Actors:',
            self.film().actors)
        print(
            'CINEMA: Nom:',
            self.cinema().name,
            'Ciutat:',
            self.cinema().address)
        print('SESSIO: ', self.time()[0], ':', self.time()[1], sep='')


class Billboard:
    _films: list[Film]
    _cinemes: list[Cinema]
    _projections: list[Projection]

    def __init__(
            self,
            films: list[Film],
            cinemes: list[Cinema],
            projections: list[Projection]) -> None:
        self._films, self._cinemes, self._projections = films, cinemes, projections

    def films(self) -> list[Film]:
        return self._films

    def projections(self) -> list[Projection]:
        return self._projections

    def cinemes(self) -> list[Cinema]:
        return self._cinemes

def read() -> Billboard:

    webs = ['https://www.sensacine.com/cines/cines-en-72480/', 
        'https://www.sensacine.com/cines/cines-en-72480/?page=2', 'https://www.sensacine.com/cines/cines-en-72480/?page=3']

    elements : list[Any] = []
    for i in range(3):
        contingut = requests.get(webs[i]).content
        soup = BeautifulSoup(contingut, 'lxml')
        elements += (soup.find_all('div', class_='item_resa'))  

   
    cinemes = llista_cinema(elements)
    films = llista_films(elements)
    projections = llista_projeccions(elements)
    
    return Billboard(films, cinemes, projections)

def adresses() -> dict[str, str]:

    webs = ['https://www.sensacine.com/cines/cines-en-72480/', 
        'https://www.sensacine.com/cines/cines-en-72480/?page=2', 'https://www.sensacine.com/cines/cines-en-72480/?page=3']

    elements : list[Any] = []
    adreces : dict[Any, Any] = dict()
    
    
    for i in range(3):
        contingut = requests.get(webs[i]).content
        soup = BeautifulSoup(contingut, 'lxml')
        elements = (soup.find_all('a', class_='no_underline j_entities'))  
        adress = (soup.find_all('span', class_='lighten'))
        j = 0  
        match : list[str] = []
        for element in elements:
            match.append(element.text.strip())
        for x in adress:
            adreça = x.text.strip()     
            if adreça[-1] == "m": continue
    
            adreces[match[j]] = adreça
            j += 1
    
    
    
    return adreces
            
def cinemes() -> dict[str, Cinema]:

    cinemes : dict[str, Cinema] = dict()
    cinemes['Arenas Multicines 3D'] = Cinema('Arenas Multicines 3D', 'Gran Via de les Corts Catalanes, 385, 08015 Barcelona', (41.3762958, 2.1493046396153845))
    cinemes['Aribau Multicines'] =Cinema('Aribau Multicines', 'Calle Aribau, 8, 08011 Barcelona', (41.386218, 2.162393))
    cinemes['Bosque Multicines'] = Cinema('Bosque Multicines', 'Rambla de Prat 16, 08012 Barcelona', (41.401519050000005, 2.1516103914622153))
    cinemes['Cinema Comedia'] = Cinema('Cinema Comedia', 'Passeig de Gracia, 13, 08007 Barcelona', (41.389718, 2.167663))
    cinemes['Cinemes Girona'] = Cinema('Cinemes Girona', 'Carrer de Girona 173-175, 08025 Barcelona', (41.399941, 2.1642872))
    cinemes['Cines Verdi Barcelona'] = Cinema('Cines Verdi Barcelona', 'Calle Verdi, 32, 08012 Barcelona', (41.403920, 2.156800))
    cinemes['Cinesa Diagonal 3D'] = Cinema('Cinesa Diagonal 3D', 'Santa Fe de Nou Mèxic s/n, 08017 Barcelona', (41.393731, 2.136119))
    cinemes['Cinesa Diagonal Mar 18'] = Cinema('Cinesa Diagonal Mar 18', 'Avinguda Diagonal, 3, 08019 Barcelona', (41.4101085, 2.2172596))
    cinemes['Cinesa La Maquinista 3D'] = Cinema('Cinesa La Maquinista 3D', 'Passeig Potosí 2 - Centre Comercial La Maquinista, 08030 Barcelona', (41.439119, 2.198340))
    cinemes['Cinesa SOM Multiespai'] = Cinema('Cinesa SOM Multiespai', 'Paseo Andreu Nin s/n - Pintor Alzamora, 08016 Barcelona', (41.435624, 2.180063))
    cinemes['Glòries Multicines'] = Cinema('Glòries Multicines', 'Avinguda Diagonal, 208, 08018 Barcelona', (41.4053714, 2.1928801))
    cinemes['Gran Sarrià Multicines'] = Cinema('Gran Sarrià Multicines', 'General Mitre, 38-44, 08017 Barcelona', (41.3991688, 2.1340682))
    cinemes['Maldá Arts Forum'] = Cinema('Maldà Arts Forum', 'Carrer del Pi, 5, 08002 Barcelona', (41.3832363, 2.1739003))
    cinemes['Renoir Floridablanca'] = Cinema('Renoir Floridablanca', 'Calle Floridablanca, 135, 08011 Barcelona', (41.381718, 2.162713))
    cinemes['Sala Phenomena Experience'] = Cinema('Sala Phenomena Experience', 'C/ Sant Antoni Maria Claret, 168, 08041 Barcelona', (41.5982715, 2.2894702))
    cinemes['Yelmo Cines Icaria 3D'] = Cinema('Yelmo Cines Icaria 3D', 'Calle Salvador Espriu, 61, 08005 Barcelona', (41.390225, 2.197470))
    cinemes['Boliche Cinemes'] = Cinema('Boliche Cinemes', 'Avinguda Diagonal, 508, 08006 Barcelona', (41.3952918, 2.1536309))
    cinemes['Zumzeig Cinema'] = Cinema('Zumzeig Cinema', 'Carrer Béjar, 53, 8014 Barcelona', (41.3773203, 2.1450266))
    cinemes['Balmes Multicines'] = Cinema('Balmes Multicines', 'Calle Balmes, 422-424, 08022 Barcelona', (41.2202618, 1.7241557))
    cinemes['Cinesa La Farga 3D'] = Cinema('Cinesa La Farga 3D', 'Avinguda Josep Tarradellas 145, 08901 L\'Hospitalet de Llobregat', (41.391084, 2.143663))
    cinemes['Filmax Gran Via 3D'] = Cinema('Filmax Gran Via 3D', 'Avinguda Gran Via 75 - Centre Comercial Gran Via 2, 08908 L\'Hospitalet de Llobregat', (41.358786, 2.128130))
    cinemes['Full HD Cinemes Centre Splau'] = Cinema('Full HD Cinemes Centre Splau', 'Centre Comercial Splau! - Avinguda Baix LLobregat, 08940 Cornella De Llobregat', (41.347255, 2.077846))
    cinemes['Cine Capri'] = Cinema('Cine Capri', 'Avinguda Virgen Montserrat, 111, 08820 Prat De Llobregat', (41.325762, 2.095167))
    cinemes['Ocine Màgic'] = Cinema('Ocine Màgic', 'Carrer de la concòrdia, 1, 08917 Badalona', (41.442599, 2.229622))
    cinemes['Cinebaix'] = Cinema('Cinebaix', 'Joan Batllori, 21, 08980 Sant Feliu De Llobregat', (41.3819167, 2.0448757))
    cinemes['Cinemes Can Castellet'] = Cinema('Cinemes Can Castellet', 'Calle Jaume I, 32, 08830 Sant Boi De Llobregat', (41.345130, 2.040618))
    cinemes['Cinemes Sant Cugat'] = Cinema('Cinemes Sant Cugat', 'Centre Cultural Sant Cugat - Avda. Pla del Vinyet s/n, 08190 Sant Cugat Del Vallès', (41.469601, 2.090266))
    cinemes['Cines Montcada'] = Cinema('Cines Montcada', 'Calle Verdi, 2, 08110 Montcada', (41.494098, 2.180340))
    cinemes['Yelmo Cines Baricentro'] = Cinema('Yelmo Cines Baricentro', 'N-150, km 6, 08210 Barcelona', (41.507579, 2.137576))
    cinemes['Yelmo Cines Sant Cugat'] = Cinema('Yelmo Cines Sant Cugat', 'Avinguda Via Augusta, 2, 08174 Sant Cugat del Vallès', (41.483465, 2.054289))
    
    
    return cinemes

def write() -> None:

    bill = read()

    """for i in range(len(bill.projections())):
        print('PROJECCIO', i)
        bill.projections()[i].escriu()
    print(len(bill.films()))
    
    """
    for j in range(len(bill.films())):
        try:
            print('PELLICULA', j)
            bill.films()[j].escriu()
        except: continue
    print(len(bill.cinemes()))
    for k in range(len(bill.cinemes())):
        print('CINEMA', k)
        bill.cinemes()[k].escriu()
        
def llista_cinema(elements: Any) -> list[Cinema]:

    cinema : dict[str, Cinema] = dict()
    cines = cinemes()
    for element in elements:
        
        content = str(element)
        match = re.search(r'data-theater=\'(.*?)\'', content)
        if match:
            theater_data = match.group(1)
            theater_list = json.loads(theater_data)
            
            cinema[theater_list['name']] = cines[theater_list['name']]
            
            
    return list(cinema.values())


def llista_films(elements: Any) -> list[Film]:

    films : dict[str, Film] = dict()
    for element in elements:
        content = str(element)
        match = re.search(r'data-movie=\'(.*?)\'', content)
        if match:
            movie_data = match.group(1)
            movie_list = json.loads(movie_data)
            
            films[movie_list['id']] = Film(movie_list)
            
            
    return list(films.values())


def llista_projeccions(elements: Any) -> list[Projection]:
    """Retorna un diccionari de cada pel·licula i temps, película, cinema."""

    projections : list[Projection] = []
    
    for element in elements:
        content = str(element)
        # Utilitza expressió regular per trobar els valors de l'atribut
        # data-times
        match = re.search(r'data-times=\'(.*?)\'', content)
        if match:
            times_data = match.group(1)
            times_list = json.loads(times_data)
                       
            time = int(times_list[0][0] + times_list[0][1]), int(times_list[0][3] + times_list[0][4])
            
        match2 = re.search(r'data-theater=\'(.*?)\'', content)
        if match2:
            theater_data = match2.group(1)
            theater_list = json.loads(theater_data)
            cinema = cinemes()[theater_list['name']]
            
        match3 = re.search(r'data-movie=\'(.*?)\'', content)
        if match3:
            movie_data = match3.group(1)
            movie_list = json.loads(movie_data)
            film = Film(movie_list)

        if match and match2 and match3:
            projections.append(Projection(film, cinema, time))

    return projections


write()
