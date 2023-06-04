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
        "Inicialitza la classe film a partir d'un diccionari amb les claus title, genre, directors i actors."
        self.title = elements['title']
        self.genre = elements['genre']
        self.director = elements['directors']
        self.actors = elements['actors']


class Cinema:
    name: str
    address: str
    coordenades: tuple[float, float]  # Latitud, longitud

    def __init__(self, name: str, address: str, coordenades: tuple[float, float]) -> None:
        "Inicialitza la classe Cinema donat el nom, adreça i coordenades, que es treuen d'una llista fixa."
        self.name = name
        self.address = address
        self.coordenades = coordenades


class Projection:
    _film: Film
    _cinema: Cinema
    _time: tuple[int, int]   # hora:minut
    # language: str de moment suda perquè no hi és a la info de Sensacine.

    def __init__(self, film: Film, cinema: Cinema,
                 time: tuple[int, int]) -> None:
        "Inicialitza la classe Projection donada una pel·licula, cinema i hora."
        self._film, self._cinema, self._time = film, cinema, time

    def film(self) -> Film:
        """Retorna la pel·licula de la projeccio."""
        return self._film

    def cinema(self) -> Cinema:
        """Retorna el cinema de la projeccio."""
        return self._cinema

    def time(self) -> tuple[int, int]:
        """Retorna l'hora de començament de la projeccio. Hora, minut"""
        return self._time


class Billboard:
    _films: list[Film]
    _cinemes: list[Cinema]
    _projections: list[Projection]

    def __init__(
            self,
            films: list[Film],
            cinemes: list[Cinema],
            projections: list[Projection]) -> None:
        """Inicialitza la classe Billboard donades una llista de pel·licules, cinemes i projeccions."""
        self._films, self._cinemes, self._projections = films, cinemes, projections

    def films(self) -> list[Film]:
        """Retorna la llista de pel·licules."""
        return self._films

    def projections(self) -> list[Projection]:
        """Retorna la llista de projeccions."""
        return self._projections

    def cinemes(self) -> list[Cinema]:
        """Retorna la llista de cinemes."""
        return self._cinemes

    def troba_mot(self, m: str) -> list[Projection]:
        """Retorna una llista de projeccions que tenen el mot m al titol de la pel·licula i nom del cinema."""
        matching_mots = [
            element for element in self.projections() if m in element.film().title or m in element.film().actors or m in element.film().director or m in element.film().genre or m in element.cinema().address]
        return matching_mots

    def troba_actor(self, m: str) -> list[Projection]:
        """Retorna una llista de projeccions les pel·licules de les qual tenen l'actor m. Prec: s'ha d'escriure el nom sencer."""
        matching_mots = [
            element for element in self.projections() if m in element.film().actors]
        return matching_mots

    def troba_director(self, m: str) -> list[Projection]:
        """Retorna una llista de projeccions les pel·licules de les qual tenen el director m. Prec: s'ha d'escriure el nom sencer."""
        matching_mots = [
            element for element in self.projections() if m in element.film().director]
        return matching_mots

    def troba_genere(self, m: str) -> list[Projection]:
        """Retorna una llista de projeccions les pel·licules de les qual són del genere m. Prec: s'ha d'escriure correctament."""
        matching_mots = [
            element for element in self.projections() if m in element.film().genre]
        return matching_mots


def sort_hora(projections: list[Projection]) -> None:
    """Ordena la llista de projeccions projections per horari de petit a gran."""
    sorted(projections, key=lambda x: x.time()[0])


def read() -> Billboard:
    """Funció principal del programa billboard que llegeix la cartellera del cinemes de Barcelona i la retorna en la classe Billboard."""
    webs = ['https://www.sensacine.com/cines/cines-en-72480/',
            'https://www.sensacine.com/cines/cines-en-72480/?page=2', 'https://www.sensacine.com/cines/cines-en-72480/?page=3']

    elements: list[Any] = []
    for i in range(3):
        contingut = requests.get(webs[i]).content
        soup = BeautifulSoup(contingut, 'lxml')
        elements += (soup.find_all('div', class_='item_resa'))

    cinemes = llista_cinema(elements)
    films = llista_films(elements)
    projections = llista_projeccions(elements)

    return Billboard(films, cinemes, projections)


def cinemes() -> dict[str, Cinema]:
    """Llista que recull les dades dels cinemes de Barcelona i les retorna com a diccionari amb el nom del cinema i el tipus Cinema."""
    cinemes: dict[str, Cinema] = dict()
    cinemes['Arenas Multicines 3D'] = Cinema(
        'Arenas Multicines 3D', 'Gran Via de les Corts Catalanes, 385, 08015 Barcelona', (2.149546, 41.376047))
    cinemes['Aribau Multicines'] = Cinema(
        'Aribau Multicines', 'Calle Aribau, 8, 08011 Barcelona', (2.162393, 41.386218))
    cinemes['Bosque Multicines'] = Cinema(
        'Bosque Multicines', 'Rambla de Prat 16, 08012 Barcelona', (2.1516103914622153, 41.401519050000005))
    cinemes['Cinema Comedia'] = Cinema(
        'Cinema Comedia', 'Passeig de Gracia, 13, 08007 Barcelona', (2.167663, 41.389718))
    cinemes['Cinemes Girona'] = Cinema(
        'Cinemes Girona', 'Carrer de Girona 173-175, 08025 Barcelona', (2.1642872, 41.399941))
    cinemes['Cines Verdi Barcelona'] = Cinema(
        'Cines Verdi Barcelona', 'Calle Verdi, 32, 08012 Barcelona', (2.156800, 41.403920))
    cinemes['Cinesa Diagonal 3D'] = Cinema(
        'Cinesa Diagonal 3D', 'Santa Fe de Nou Mèxic s/n, 08017 Barcelona', (2.136119, 41.393731))
    cinemes['Cinesa Diagonal Mar 18'] = Cinema(
        'Cinesa Diagonal Mar 18', 'Avinguda Diagonal, 3, 08019 Barcelona', (2.2172596, 41.4101085))
    cinemes['Cinesa La Maquinista 3D'] = Cinema(
        'Cinesa La Maquinista 3D', 'Passeig Potosí 2 - Centre Comercial La Maquinista, 08030 Barcelona', (2.198340, 41.439119))
    cinemes['Cinesa SOM Multiespai'] = Cinema(
        'Cinesa SOM Multiespai', 'Paseo Andreu Nin s/n - Pintor Alzamora, 08016 Barcelona', (2.180063, 41.435624))
    cinemes['Glòries Multicines'] = Cinema(
        'Glòries Multicines', 'Avinguda Diagonal, 208, 08018 Barcelona', (2.1928801, 41.4053714))
    cinemes['Gran Sarrià Multicines'] = Cinema(
        'Gran Sarrià Multicines', 'General Mitre, 38-44, 08017 Barcelona', (2.1340682, 41.3991688))
    cinemes['Maldà Arts Forum'] = Cinema(
        'Maldà Arts Forum', 'Carrer del Pi, 5, 08002 Barcelona', (2.1739003, 41.3832363))
    cinemes['Renoir Floridablanca'] = Cinema(
        'Renoir Floridablanca', 'Calle Floridablanca, 135, 08011 Barcelona', (2.162713, 41.381718))
    cinemes['Sala Phenomena Experience'] = Cinema(
        'Sala Phenomena Experience', 'C/ Sant Antoni Maria Claret, 168, 08025 Barcelona', (2.171631, 41.408865))
    cinemes['Yelmo Cines Icaria 3D'] = Cinema(
        'Yelmo Cines Icaria 3D', 'Calle Salvador Espriu, 61, 08005 Barcelona', (2.197470, 41.390225))
    cinemes['Boliche Cinemes'] = Cinema(
        'Boliche Cinemes', 'Avinguda Diagonal, 508, 08006 Barcelona', (2.1536309, 41.3952918))
    cinemes['Zumzeig Cinema'] = Cinema(
        'Zumzeig Cinema', 'Carrer Béjar, 53, 08014 Barcelona', (2.1450266, 41.3773203))
    cinemes['Balmes Multicines'] = Cinema(
        'Balmes Multicines', 'Calle Balmes, 422-424, 08022 Barcelona', (2.139344, 41.407308))
    cinemes['Maldá Arts Forum'] = Cinema(
        'Maldà Arts Forum', 'Carrer del Pi, 5, 08002 Barcelona', (2.1739003, 41.3832363))
    # Només hem afegit els cinemes dins el municipi de Barcelona, una part de la cartellera de Sensacine s'ha tret.
    return cinemes


def llista_cinema(elements: Any) -> list[Cinema]:
    """Donat un fitxer html que conté els elements dels cinemes en retorna una llista d'ells."""
    cinema: dict[str, Cinema] = dict()
    cines = cinemes()
    for element in elements:

        content = str(element)
        match = re.search(r'data-theater=\'(.*?)\'', content)
        if match:
            theater_data = match.group(1)
            theater_list = json.loads(theater_data)
            try:
                cinema[theater_list['name']] = cines[theater_list['name']]
            except:
                continue
    return list(cinema.values())


def llista_films(elements: Any) -> list[Film]:
    """Donat un fitxer html que conté els elements de les pel·licules en retorna una llista d'ells."""
    films: dict[str, Film] = dict()
    for element in elements:
        content = str(element)
        match = re.search(r'data-movie=\'(.*?)\'', content)
        if match:
            movie_data = match.group(1)
            movie_list = json.loads(movie_data)

            films[movie_list['id']] = Film(movie_list)

    return list(films.values())


def llista_projeccions(elements: Any) -> list[Projection]:
    """Donat un fitxer html que conté els elements de les projeccions en retorna una llista d'ells."""
    projections: list[Projection] = list()
    repetits: dict[str, set[str]] = dict()
    for element in elements:

        content = str(element)
        # Utilitza expressió regular per trobar els valors de l'atribut
        # data-times
        match2 = re.search(r'data-theater=\'(.*?)\'', content)
        if match2:
            theater_data = match2.group(1)
            theater_list = json.loads(theater_data)
            try:
                cinema = cinemes()[theater_list['name']]
            except:
                continue
        match3 = re.search(r'data-movie=\'(.*?)\'', content)
        if match3:
            movie_data = match3.group(1)
            movie_list = json.loads(movie_data)
            film = Film(movie_list)

        ul_element = element.find('ul', class_='list_hours')
        em_elements = ul_element.find_all('em')
        data_times = [em.get('data-times') for em in em_elements]
        for dt in data_times: # S'agafen totes les projeccions per la pel·lícula i cinema actuals. S'eviten repeticions i agafar la informació dels dies següents.
            if cinema.name not in cinemes().keys():
                break
            time = int(dt[2] + dt[3]), int(dt[5] + dt[6])
            if match2 and match3:
                if cinema.name in repetits:
                    if film.title in repetits[cinema.name]:
                        break
                else:
                    repetits[cinema.name] = set()
                projections.append(Projection(film, cinema, time))
        repetits[cinema.name].add(film.title)
    return list(projections)
