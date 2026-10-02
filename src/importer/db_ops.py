import sqlite3
import rom_dataclasses as rdc

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

def checkDuplicateSystem(system: rdc.System, cursor: sqlite3.Cursor)->bool:
    cursor.execute("SELECT SystemName FROM Systems WHERE SystemName=?", (system.name,))
    matches = cursor.fetchall()
    return len(matches) > 0

def checkDuplicateGame(sha256: str, cursor: sqlite3.Cursor)->bool:
    cursor.execute("SELECT SHA256 FROM Games WHERE SHA256=?", (sha256,))
    matches = cursor.fetchall()
    return len(matches) > 0
 
def insertSystem(system: rdc.System, cursor: sqlite3.Cursor)->None:
    # Does not check if the system is a duplicate.

    # Determine insertion index
    cursor.execute("SELECT COUNT (*) FROM Systems")
    count = cursor.fetchone()
    sysIndex = count[0] + 1

    cursor.execute("INSERT INTO Systems (SystemID, SystemName) Values (?, ?)", (sysIndex, system.name,))

def insertGame(game: rdc.Game, systemIndex: int, cursor: sqlite3.Cursor)->None:
    # Does not check if the game is a duplicate.

    # Determine insertion index
    cursor.execute("SELECT COUNT (*) FROM Games")
    count = cursor.fetchone()
    gameIndex = count[0] + 1

    cursor.execute("INSERT INTO Games (GameID, SystemID, Filename, GameName, Path, SHA256, Publisher, GameRlsYr) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (gameIndex, systemIndex, game.filename, game.name, game.path, game.sha256, game.publisher, game.release_year,)
            )

def getSystemIndex(system: rdc.System, cursor: sqlite3.Cursor)->int:
    cursor.execute("SELECT SystemID FROM Systems WHERE SystemName=?", (system.name,))
    matches = cursor.fetchone()
    return matches[0]

