from dataclasses import dataclass # more convenient than standard classes for roms
from pathlib import Path # makes file/folder i/o more convenient
import sys # for CL i/o
#import Taskiq # for async database updates

# TODO: add more systems and add name variations
RECOGNIZED_SYSTEMS = {
    '.gba': 'gba',
    '.gbc': 'gbc',
    '.nes': 'nes',
    '.sfc': 'snes',
    '.smc': 'snes',
    '.nds': 'nds',
    '.rvz': 'gc',
    '.iso': 'variable',
    '.chd': 'variable'
}

@dataclass
class Rom: # ROM data object
    filename: str
    #region: str # no scraping yet
    #release year: str # no scraping yet
    system: str
    filepath: Path
    sha256: str # for duplicate control

def main():
    print("Starting scanner...")
    
    # TODO: dynamic input
    roms_directory = Path('~/Desktop/roms/').expanduser() # Rom directory location

    # TODO: Long term the roms don't need to be stored like this. Examine the
    # directory, get the rom + info, and create a task for a Taskiq worker
    # that handles all the data processing while the importer grabs the next item. 
    # This way you can have multiple brokers updating the database in concert
    # instead of one after the other. This is just proof of concept.
    located_roms= {'nes': [], 'snes': [], 'gbc': [], 'gba': [], 'nds': [], 'variable': []}
    
    for file in roms_directory.rglob('*'): # recursively search provided directory
        extension = file.suffix # extract extension
        if extension in RECOGNIZED_SYSTEMS: # verify if found file is a game from a recognized system
            rom = Rom(
                filename=file.name,
                system=RECOGNIZED_SYSTEMS[extension],
                filepath=file,
                sha256='0'
            ) # create rom data object

            # add to located roms dict
            located_roms.get(rom.system).append(file.name)

i __name__ == "__main__":
    main()
