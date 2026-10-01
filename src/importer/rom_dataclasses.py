from dataclasses import dataclass
from pathlib import Path
"""
These serve no purpose. This is a great example of "Just because it looks professional doesn't mean it's the best approach".

These classes serve only to hold onto data briefly until it is written to the DB and then they are discarded. You get the metadata, populate
these objects, and then pass them into a function that pulls that data out, puts it somewhere else, and discards the container. Just skip
it altogether and add the data directly into the DB instead of using a middleman. If you could somehow dynamically add the data to the 
class then they would be worth it, but you have to manually write their structure anyway. You aren't really saving yourself any time.

Will keep the file in case they provide value later.
"""
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
    release_year: str
    sha256: str
    #TODO: add methods?
    #TODO: add defaults for if data is not found?

@dataclass
class Rom: # ROM data object
    game: Game
    system: System
    path: Path
    #TODO: add methods?