from dataclasses import dataclass

@dataclass
class System: # System data object
    name: str
    #manufacturer: str
    #release_year: int 

@dataclass
class Game: # Game data object
    filename: str
    name: str
    publisher: str
    release_year: str
    path: str
    sha256: str