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

    def __init__(self, elements: dict[str, str]) -> None:
        self.name = elements['name']
        self.address = elements['city']

    def escriu(self) -> None:
        print(
            'CINEMA: Nom:',
            self.name,
            'Ciutat:',
            self.address)
        
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


def write() -> None:

    bill = read()

    for i in range(len(bill.projections())):
        print('PROJECCIO', i)
        bill.projections()[i].escriu()
    print(len(bill.films()))
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
    for element in elements:
        
        content = str(element)
        match = re.search(r'data-theater=\'(.*?)\'', content)
        if match:
            theater_data = match.group(1)
            theater_list = json.loads(theater_data)
            
            cinema[theater_list['name']] = Cinema(theater_list)
            
            
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
            cinema = Cinema(theater_list)
            
        match3 = re.search(r'data-movie=\'(.*?)\'', content)
        if match3:
            movie_data = match3.group(1)
            movie_list = json.loads(movie_data)
            film = Film(movie_list)

        if match and match2 and match3:
            projections.append(Projection(film, cinema, time))

    return projections


write()
