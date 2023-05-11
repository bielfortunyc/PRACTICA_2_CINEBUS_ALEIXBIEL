from dataclasses import dataclass

@dataclass 
class Film: 
    title: str
    genre: str
    director: str
    actors: list[str]
    ...
    
class Cinema: 
    name: str
    address: str
    ...
    
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

def read() -> Billboard: ...