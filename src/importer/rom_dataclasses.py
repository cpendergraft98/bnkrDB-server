from dataclasses import dataclass
from pathlib import Path

@dataclass
class System: # System data object
    name: str
    #manufacturer: str # need system metadata scraping
    #release_year: int # need system metadata scraping
    #TODO: add methods?
    #TODO: add defaults for if data is not found?

@dataclass
class Game: # Game data object
    filename: str
    name: str
    publisher: str
    regions: dict 
    AIdescription: str
    release_year: str
    sha256: str
    #TODO: add methods?
    #TODO: add defaults for if data is not found?

@dataclass
class Rom: # ROM data object
    game: Game
    system: System
    filepath: Path
    #TODO: add methods?