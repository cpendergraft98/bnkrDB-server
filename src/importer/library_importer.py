from pathlib import Path # makes file/folder i/o more convenient
import hashlib # for computing SHA-256 hash
import rom_dataclasses as rdc
from metadata_scraper import hasheousSearch

RECOGNIZED_EXTENSIONS = {
    '.gb': 'Game Boy',
    '.gbc': 'Game Boy Color',
    '.gba': 'Game Boy Advance',
    '.nes': 'Nintendo Entertainment System',
    '.nez': 'Nintendo Entertainment System',
    '.sfc': 'Super Nintendo Entertainment System',
    '.smc': 'Super Nintendo Entertainment System',
    '.nds': 'Nintendo DS',
    '.srl': 'Nintendo DS',
    '.cia': 'Nintendo 3DS',
    '.3ds': 'Nintendo 3DS',
    '.dsi': 'DSiWare',
    '.n64': 'Nintendo 64',
    '.ndd': 'Nintendo 64',
    '.z64': 'Nintendo 64',
    '.v64': 'Nintendo 64',
    '.rvz': 'GameCube',
    '.gcm': 'GameCube',
    '.gcz': 'GameCube',
    '.nsp': 'Nintendo Switch',
    '.xci': 'Nintendo Switch',
    '.dnsp': 'Nintendo Switch',
    '.dxci': 'Nintendo Switch',
    '.xiso': 'Xbox',
    '.cdi': 'Dreamcast',
    '.sms': 'Sega Master System',
    '.gen': 'Sega Genesis',
    '.md': 'Sega Genesis',
    '.gen': 'Sega Genesis',
    '.wud': 'Wii U',
    '.wux': 'Wii U',
    '.wua': 'Wii U',
    '.vpk': "Playstation Vita",
    '.apk': 'Android',
    '.wad': 'variable', # Wii and DoomEngine games
    '.cci': 'variable', # Xbox disc image and citra-based 3ds
    '.rvz': 'variable', # GC and Wii
    '.gcz': 'variable', # GC and Wii
    '.iso': 'variable', # Many systems
    '.chd': 'variable' # Many systems
    
}

def main():
    print("Starting scanner...")
    
    # TODO: dynamic input
    roms_directory = Path('~/OneDrive/Desktop/bnkrDB/tests/importer_test_directory').expanduser() # Rom directory location

    located_roms= []
    
    for file in roms_directory.rglob('*'): # recursively search provided directory
        extension = file.suffix
        if extension in RECOGNIZED_EXTENSIONS: 
            if RECOGNIZED_EXTENSIONS[extension] == 'variable':
                # TODO: handle file extensions that map to different systems
                continue
            else:
                #hash rom file
                sha256 = hashlib.sha256()
                sha1 = hashlib.sha1()
                with open(file, "rb") as f:
                    # loop allows for processing both SHA-256 and SHA-1 in a single pass
                    while chunk := f.read(1024 * 1024): # you found the walrus!
                        sha256.update(chunk)
                        sha1.update(chunk)

                hash256 = sha256.hexdigest()
                hash1 = sha1.hexdigest()

                #build data objects
                new_system = rdc.System(name=RECOGNIZED_EXTENSIONS[extension])
                new_game = rdc.Game(title = file.name, sha256=hash256, sha1=hash1)      
                rom = rdc.Rom(game=new_game, system=new_system, filepath=file)

                located_roms.append(rom)

    hasheousSearch(located_roms[0])

if __name__ == "__main__":
    main()
