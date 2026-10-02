from pathlib import Path # makes file/folder i/o more convenient
import hashlib # for computing SHA-256 hash
import rom_dataclasses as rdc
from metadata_scraper import hasheousSearch
import sqlite3
from recognized_extensions import RECOGNIZED_EXTENSIONS
from dotenv import load_dotenv
import os
import db_ops

load_dotenv() #load environment variables

def romImporter(romDirectoryPath: str)->None:
    print("Starting scanner...")
    
    roms_directory = Path(romDirectoryPath).expanduser() # Rom directory location

    # create/connect to database
    connection = sqlite3.connect("./src/server/bnkr.db")
    cursor = connection.cursor()

    # determine if the database has been built prior
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

    if cursor.fetchone() is None: # first-time creation of the db
        db_ops.buildDatabase(cursor)

    for file in roms_directory.rglob('*'): # recursively search provided directory
        extension = file.suffix
        if extension in RECOGNIZED_EXTENSIONS: 
            if RECOGNIZED_EXTENSIONS[extension] == 'variable':
                # TODO: handle file extensions that map to different systems
                continue
            else:
                #hash rom file
                sha256 = hashlib.sha256()
                sha1 = hashlib.sha1() # used to search Hasheous
                with open(file, "rb") as f:
                    # loop allows for processing both SHA-256 and SHA-1 in a single pass
                    while chunk := f.read(1024 * 1024): # you found the walrus!
                        sha256.update(chunk)
                        sha1.update(chunk)

                hash256 = sha256.hexdigest()
                if not db_ops.checkDuplicateGame(hash256, cursor): # check for duplicate game
                    hash1 = sha1.hexdigest()

                    metadata = hasheousSearch(hash1)

                    # if metadata is nonetype then Hasheous returned 404
                    if metadata != None:

                        system = rdc.System(
                            name=RECOGNIZED_EXTENSIONS[extension],
                            #manufacturer=,
                            #releaseYear=,
                        )

                        game = rdc.Game(
                            filename=file.name,
                            name=metadata['name'],
                            publisher=metadata['publisher'],
                            release_year=metadata['release_year'],
                            path=str(file),
                            sha256=hash256
                        )

                        # check for duplicate system
                        if not db_ops.checkDuplicateSystem(system, cursor):
                            db_ops.insertSystem(system, cursor) # insert if duplicate not found

                        # determine system index
                        sysIndex = db_ops.getSystemIndex(system, cursor)

                        #insert the game
                        db_ops.insertGame(game, sysIndex, cursor)

                else:
                    print("Duplicate game identified. Skipping....")

    connection.commit()
    connection.close()

if __name__ == "__main__":
    #TODO: Standardize filepath format for storage? SHould be linux if server runs linux
    romImporter(os.getenv("LINUX_PATH"))
