from pathlib import Path # makes file/folder i/o more convenient
import hashlib # for computing SHA-256 hash
import rom_dataclasses as rdc
from metadata_scraper import hasheousSearch
import sqlite3
from recognized_extensions import RECOGNIZED_EXTENSIONS

def buildDatabase(cursor: sqlite3.Cursor)->None:
    # build database in-placE

    # user table
    cursor.execute("""
        CREATE TABLE Users(
            UserID INTEGER PRIMARY KEY,
            UserName TEXT UNIQUE,
            PasswdHash TEXT NOT NULL
        )
    """)

    # system table
    cursor.execute("""
        CREATE TABLE Systems(
            SystemID INTEGER PRIMARY KEY,
            SystemName TEXT UNIQUE,
            Manufacturer TEXT,
            SysRlsYr TEXT
        )
    """)

    # game table
    cursor.execute("""
        CREATE TABLE Games(
            GameID INTEGER PRIMARY KEY,
            SystemID INTEGER,
            Filename TEXT NOT NULL,
            GameName TEXT NOT NULL,
            Path TEXT NOT NULL,
            SHA256 TEXT UNIQUE,
            Publisher TEXT,
            GameRlsYr TEXT,
            CONSTRAINT fk_Systems
            FOREIGN KEY (SystemID)
            REFERENCES Systems(SystemID)
        )
    """)

    # favorites table
    cursor.execute("""
        CREATE TABLE Favorites(
            UserID INTEGER,
            GameID INTEGER,
            CONSTRAINT fk_Users
            FOREIGN KEY (UserID)
            REFERENCES Users(UserID)
            CONSTRAINT fk_Games
            FOREIGN KEY (GameID)
            REFERENCES Games(GameID)
        )
    """)


def romImporter(romDirectoryPath: str)->None:
    print("Starting scanner...")
    
    roms_directory = Path(romDirectoryPath).expanduser() # Rom directory location

    # create/connect to database
    connection = sqlite3.connect("./src/server/bnkr.db")
    cursor = connection.cursor()

    # determine if the database has been built prior
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

    if cursor.fetchone() is None: # first-time creation of the db
        buildDatabase(cursor)

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
                hash1 = sha1.hexdigest()

                metadata = hasheousSearch(hash1)

                # if metadata is nonetype then Hasheous returned 404
                if metadata != None:

                    # Game entry data
                    cursor.execute("SELECT * FROM Games") #determines ID
                    gameIndex = len(cursor.fetchall())
                    filename = file.name
                    gameName = metadata['name']
                    publisher = metadata['publisher']
                    rlsYr = metadata['release_year']

                    #TODO: Create a function to check for duplicates in game table based off SHA256

                    # system entry data
                    cursor.execute('SELECT SystemName FROM Systems') #determines ID
                    existing_names = cursor.fetchall()
                    sysIndex = len(existing_names)
                    systemName = RECOGNIZED_EXTENSIONS[extension]

                    print(existing_names)
                    print(systemName)
                    #AHHHHHHHHHHHHHHHHHHHHHHHH
                    if systemName not in existing_names: # System hasn't been entered into database
                        cursor.execute("INSERT INTO Systems (SystemID, SystemName) Values(?, ?)", [sysIndex, systemName])
                    else: # System exists in database, extract id for game entry
                        cursor.execute("SELECT SystemID FROM Systems WHERE SystemName=?", systemName)
                        sysIndex = cursor.fetchone()

                    cursor.execute("INSERT INTO Games (GameId, SystemId, Filename, GameName, Path, SHA256, Publisher, GameRlsYr) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                                [gameIndex, sysIndex, filename, gameName, str(file), hash256, publisher, rlsYr]
                        )
    connection.close()

if __name__ == "__main__":
    romImporter("C:/Users/cpend/OneDrive/Desktop/bnkrDB/tests/importer_test_directory")
