from dataclasses import dataclass # more convenient than standard classes for roms
from pathlib import Path # makes file/folder i/o more convenient
import sys # for CL i/o

# TODO: add more systems and add name variations (i.e. sfc and snes recognized as the same console)
RECOGNIZED_SYSTEMS = {
    '.gba': 'gba',
    '.gbc': 'gbc',
    '.nes': 'nes',
    '.sfc': 'snes',
    '.smc': 'snes',
    '.nds': 'nds',
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

    # Stores located roms for later printing
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

    for x in located_roms:
        print("System: ", x.upper())
        for i in located_roms.get(x):
            print(" ", i)
        print('\n')

if __name__ == "__main__":
    main()
