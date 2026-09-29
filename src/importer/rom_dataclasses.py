from dataclasses import dataclass
from pathlib import Path

@dataclass
class System: # System data object
    name: str
    #manufacturer: str # need metadata scraping
    #release_year: int # need metadata scraping
    #TODO: add methods?

@dataclass
class Game: # Game data object
    title: str
    #region: str # need metadat scraping
    #release_year: int # need metadata scraping
    sha256: str # need to build the hashing logic
    sha1: str # used for metadata extraction
    #TODO: add methods?

@dataclass
class Rom: # ROM data object
    game: Game
    system: System
    filepath: Path
    #TODO: add methods?