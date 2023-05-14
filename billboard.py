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
    
    def __init__(self, title: str, genre: str, director: str, actors: list[str]) -> None:
        title = title
        genre = genre
        director = director
        actors = actors
    
class Cinema: 
    name: str
    address: str
    def __init__(self, name, address) -> None:
        name = name
        address = address
    
class Projection: 
    film: Film
    cinema: Cinema
    time: tuple[int, int]   # hora:minut
    language: str
    ...
    
class Billboard: 
    films: list[Film]
    cinemas: list[Cinema]
    projections: list[Projection]

def read() -> Billboard:
    
    informacio_webs = web_scraping('https://www.sensacine.com/cines/cines-en-72480/')
    informacio_webs2 = web_scraping('https://www.sensacine.com/cines/cines-en-72480/?page=2')
    informacio_webs3 = web_scraping('https://www.sensacine.com/cines/cines-en-72480/?page=3')

    informacio_total = {**informacio_webs, ** informacio_webs2, **informacio_webs3}
    cinemes = llista_cinemes()
    films = llista_films()

def web_cinemes(s: str) -> dict[str, dict[str, str]]:
    """Retorna el fitxer amb cinemes."""
    cinemes : dict[str, dict[str,str]] = dict()
    
    contingut_html = requests.get(s).content
    soup = BeautifulSoup(contingut_html, 'html.parser')
    elements = soup.find_all(class_='item_resa')

    for element in elements:
        content = str(element)
        match = re.search(r'data-theater=\'(.*?)\'', content)
        if match:
            theater_data = match.group(1)
            theater_list = json.loads(theater_data)
            cinemes['name'] = theater_list
    
    return cinemes
    
def llista_cinemes() -> list[Cinema]:
    
    c1 = web_cinemes('https://www.sensacine.com/cines/cines-en-72480/')
    c2 = web_cinemes('https://www.sensacine.com/cines/cines-en-72480/?page=2')
    c3 = web_cinemes('https://www.sensacine.com/cines/cines-en-72480/?page=3')

    cinemes = {**c1, **c2, **c3}
    
    llista : list[Cinema] = list()
    for element in cinemes.values():
        cinema = Cinema(element['name'], element['city'])
        llista.append(cinema)
    
    return llista

def web_movies(s: str) -> dict[str, dict[str, Any]]:
    """Retorna el fitxer amb cinemes."""
    movies : dict[str, dict[str, Any]] = dict()
    
    contingut_html = requests.get(s).content
    soup = BeautifulSoup(contingut_html, 'html.parser')
    elements = soup.find_all(class_='item_resa')

    for element in elements:
        content = str(element)
        match = re.search(r'data-movies=\'(.*?)\'', content)
        if match:
            theater_data = match.group(1)
            theater_list = json.loads(theater_data)
            movies['name'] = theater_list
    
    return movies
    
def llista_films() -> list[Film]:
    
    c1 = web_movies('https://www.sensacine.com/cines/cines-en-72480/')
    c2 = web_movies('https://www.sensacine.com/cines/cines-en-72480/?page=2')
    c3 = web_movies('https://www.sensacine.com/cines/cines-en-72480/?page=3')

    movies = {**c1, **c2, **c3}
    
    llista : list[Film] = list()
    for element in movies.values():
        movie = Film(element['title'], element['genre'], element['directors'], element['actors'])
        llista.append(movie))
    
    return llista
    
def web_scraping(s: str) -> dict[str, list[list[Any]]]:
    """Retorna un diccionari de cada pel·licula i temps, película, cinema."""
    contingut_html = requests.get(s).content
    soup = BeautifulSoup(contingut_html, 'html.parser')
    elements = soup.find_all(class_='item_resa')

    result : dict[str, list[list[Any]]] = {}

    for element in elements:
        content = str(element)

        # Utilitza expressió regular per trobar els valors de l'atribut data-times
        match = re.search(r'data-times=\'(.*?)\'', content)
        if match:
            times_data = match.group(1)
            times_list = json.loads(times_data)

        match2 = re.search(r'data-theater=\'(.*?)\'', content)
        if match2:
            theater_data = match2.group(1)
            theater_list = json.loads(theater_data)

        match3 = re.search(r'data-movie=\'(.*?)\'', content)
        if match3:
            movie_data = match3.group(1)
            movie_list = json.loads(movie_data)
    
        result[movie_list['title']] = [movie_list, theater_list, times_list]
    
    return result

