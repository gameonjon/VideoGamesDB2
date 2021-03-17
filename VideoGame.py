import sqlite3
from sqlite3 import Error
import time

def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")
    return conn


def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def createTables(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create tables")


            #==================================
            #STILL NEED CONNECTION TO SOME 
    try:
        sql = """CREATE TABLE Games (
                    g_title varchar(30) NOT NULL,
                    g_year DATE NOT NULL,
                    g_genre varchar(15),
                    g_exkey decimal(5,0),
                    g_gameID INTEGER PRIMARY KEY AUTOINCREMENT                   
                    )"""
                    # g_pubkey decimal(12,0) NOT NULL,
                    # g_devkey decimal(12,0) NOT NULL
        _conn.execute(sql)

        sql = """CREATE TABLE Contracts (
                    c_gameID INTEGER,
                    c_pubkey INTEGER,
                    c_devkey INTEGER,
                    FOREIGN KEY (c_gameID) REFERENCES Games(g_gameID),
                    FOREIGN KEY (c_pubkey) REFERENCES Publisher(p_pubkey),
                    FOREIGN KEY (c_devkey) REFERENCES Developer(d_devkey)
                )"""
        _conn.execute(sql)

        sql = """CREATE TABLE Platform (
                    pf_system varchar(25) NOT NULL,
                    pf_exkey decimal(5,0) NOT NULL,
                    pf_exclusive boolean NOT NULL
                    )"""
        _conn.execute(sql)

        sql = """CREATE TABLE Reviews (
                    r_gameID INTEGER NOT NULL,
                    r_rating decimal(2,1) NOT NULL,
                    r_resource varchar(25) NOT NULL,
                    r_comment VARCHAR(50))"""
        _conn.execute(sql)

        sql = """CREATE TABLE Publisher (
                    p_name varchar(30) NOT NULL,
                    p_pubkey INTEGER PRIMARY KEY AUTOINCREMENT
                )"""
        _conn.execute(sql)

        sql = """CREATE TABLE Developer (
                    d_name varchar(30) NOT NULL,
                    d_devkey INTEGER PRIMARY KEY AUTOINCREMENT
                )"""
        _conn.execute(sql)

        sql = """CREATE TABLE GamePlay (
                    gp_gameID INTEGER NOT NULL,
                    gp_url varchar(15) NOT NULL,
                    gp_platform varchar(30) NOT NULL
                )"""
        _conn.execute(sql)

        _conn.commit()
        print("success")
    
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def dropTables(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")

    try: 
        sql = "DROP TABLE Games"
        _conn.execute(sql)

        sql = "DROP TABLE Contracts"
        _conn.execute(sql)

        sql = "DROP TABLE Platform"
        _conn.execute(sql)

        sql = "DROP TABLE Reviews"
        _conn.execute(sql)

        sql = "DROP TABLE Publisher"
        _conn.execute(sql)

        sql = "DROP TABLE Developer"
        _conn.execute(sql)

        sql = "DROP TABLE GamePlay"
        _conn.execute(sql)

        _conn.commit()
        print("success")

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def populateTable_Games(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate table")

    try:

        games = [               #(title, year, genre, exkey, gameID )   #pubkey, devkey)

            #Platform:
            # ps4, xbox1, xbox360, MSW, Mac OS, Linux
            ("Rise of the Tomb Raider", '2016-02-09', "action-adventure", 11, 1),# 10001, 20001),
            #Platform: ps4, xbox1, MSW
            ("Star Wars Jedi: Fallen Order",'2019-11-15', "action-adventure", 11, 2),# 10004, 20005),
            #Platform: ps4, xbox1, MSW
            ("Star Wars: BattleFront 2", '2017-11-17', "shooter", 11, 3), #10004, 20006),
            #Platform: ps4, MSW
            ("Death Stranding", '2019-11-08', "action", 5, 4), # 10006, 20009),
            #Platform: ps4, nintendo switch, xbox 1, msw
            ("Overwatch", "2016-05-24", "shooter", 13, 5), #10007, 20010),
            #Platform: ps4, xbox1, msw, nintendo switch
            ("Bioshock: The Collection", '2016-09-13', "shooter", 13, 6), #10008, 20012),
            #Platform: ps4, xbox1, msw, linux, classic Mac os
            ("Dying Light", '2015-01-26', "action", 11, 7), # 10010, 20017), 
            #Platform: ps4, xbox1, ps3, xbox360, msw
            ("Battlefield 4", '2013-10-29', "shooter", 11, 8), # 10004, 20006),
            #Platform: ps4, xbox1, msw
            ("Call of Duty: Modern Warfare Remastered", '2016-11-04', "shooter", 11, 9), #10012, 20018),
            #Platform: ps4, xbox1, msw
            ("Tom Clancy's Ghost Recon", '2017-03-07', "tactical shooter", 11, 10), #10013, 20021),
            #Platform: ps4 
            ("Killzone Shadow Fall", '2013-11-15', "shooter", 1, 11), # 10005, 20024),
            #Platform: ps4
            ("The Last of Us Remastered", '2014-07-29', "survival-horror", 1, 12), #10005, 20025),
            #Platform: ps4, msw, xbox1
            ("Star Wars: Battlefront", '2015-11-16', "shooter", 11, 13), #10004, 20006),
            #Platform: ps4, msw
            ("Horizor Zero Dawn", '2017-02-28', "action", 5, 14), #10005, 20024),
            #Platform: ps4, xbox1, msw
            ("Battlefield 1", '2016-10-21', "shooter", 11, 15), #10004, 20006),
            #Platform: ps4, xbox1, msw
            ("Need for Speed", '2015-11-03', "racing", 11, 16), # 10004, 20026),
            #Platform: ps4
            ("Spider-Man", '2018-09-07', "action-adventure", 1, 17), #10005, 20027),
            #Platform: ps4, xbox1, msw
            ("Call of Duty: Modern Warfare", '2019-08-23', "shooter", 11, 18), #10012, 20018)
        ]
        sql = "INSERT INTO Games VALUES(?, ?, ?, ?, ?)"
        _conn.executemany(sql, games)

        _conn.commit()
        print("success")

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def populate_Contracts(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate Contracts between Games, Publsihers and developers")

    try:
        contract = [ # contracts ( gameID, pubkey, devkey)
            #rise of the tomb raider
            (1, 10001, 20001),
            (1,10002, 20002),
            (1, 10003, 20003),
            (1, "NULL", 20004),
            #Star  wars jedi fallen order
            (2, 10004, 20005),
            #star wars : battlefront 2
            (3, 10004, 20006),
            (3, '\0', 20007),
            (3, '\0', 20008),
            #death stranding
            (4, 10005, 20009),
            (4, 10006, '\0'),
            #overwatch
            (5, 10007, 20010),
            (5, '\0', 20011),
            #bioshock the collection
            (6, 10008, 20012),
            (6, '\0', 20013),
            (6, '\0', 20014),
            (6, '\0', 20015),
            (6, '\0', 20016),
            #dying light
            (7, 10010, 20017),
            (7, 10011, '\0'),
            #battlefield 4
            (8, 10004, 20006),
            (8, '\0', 20029),
            #COD mw remastered
            (9, 10012, 20018),
            (9, '\0', 20019),
            (9, '\0', 20020),
            #tom clancy ghost recon
            (10, 10013, 20021),
            (10, 10014, 20022),
            (10, 10015, 20023),
            (10, 10016, 20030),
            (10, '\0', 20031),
            (10, '\0', 20032),
            (10, '\0', 20033),
            (10, '\0', 20034),
            (10, '\0', 20035),
            (10, '\0', 20036),
            (10, '\0', 20037),
            (10, '\0', 20038),
            (10, '\0', 20039),
            (10, '\0', 20040),
            (10, '\0', 20041),
            (10, '\0', 20042),
            (10, '\0', 20043),
            (10, '\0', 20044),
            (10, '\0', 20045),
            (10, '\0', 20046),
            (10, '\0', 20047),
            (10, '\0', 20048),
            #killzone shadow fall
            (11, 10005, 20024),
            #TLOU Remastered
            (12, 10005, 20025),
            #star wars battlefront
            (13, 10004, 20006),
            (13, '\0', 20008),
            #horizon zero dawn
            (14, 10005, 20024),
            #Battlefield 1
            (15, 10004, 20006),
            #need for speed
            (16, 10004, 20049),
            #spider man
            (17, 10005, 20027),
            (17, 10017, '\0'),
            #cod MW 2019
            (18, 10012, 20018),
            (18, '\0', 20028)
        ]
        sql = "INSERT INTO Contracts VALUES(?, ?, ?)"
        _conn.executemany(sql, contract)

        _conn.commit()
        print("success")

    except Error as e:
        _conn.rollback()
        print(e)

print("++++++++++++++++++++++++++++++++++")



def populateTable_DevPub(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate Developer and Publisher tables:")

    try: 
        pub = [
            ("Square Enix", 10001),
            ("Feral Interactive", 10002),
            ("Xbox Game Studios", 10003),
            ("Electronic Arts", 10004),
            ("Sony Interactive Entertainment", 10005),
            ("505 Games", 10006), 
            ("Blizzard Entertainment", 10007), 
            ("2K Games", 10008),
            ("Take-Two Interactive", 10009),
            ("Techland", 10010),
            ("Warner Bros. Interactive Entertainment", 10011),
            ("Activision", 10012),
            ("Ubisoft", 10013),
            ("Gameloft", 10014),
            ("Aspyr", 10015),
            ("Frontier Groove, Inc.", 10016),
            ("Sony Interactive Entertainment Europe", 10017)

        ]
        sql = "INSERT INTO Publisher Values(?, ?)"
        _conn.executemany(sql, pub)

        dev = [
            ("Crystal Dynamics", 20001),
            ("Eidos-Montreal", 20002),
            ("Feral Interactive", 20003),
            ("Cameron Suey", 20004),
            ("Respawn Entertainment", 20005),
            ("DICE", 20006),
            ("Motive Studios", 20007),
            ("Criterion Software", 20008),
            ("Kojima Productions", 20009),
            ("Blizzard Entertainment", 20010),
            ("Iron Galaxy", 20011),
            ("Irrational Games", 20012),
            ("2K Marin", 20013),
            ("2K Australia", 20014),
            ("Blind Squirrel Games", 20015),
            ("Digital Extremes", 20016),
            ("Techland", 20017),
            ("Infinity Ward", 20018),
            ("Raven Software", 20019),
            ("Beenox", 20020),
            ("Ubisoft", 20021),
            ("Ubisoft Paris", 20022),
            ("Red Storm Entertainment", 20023),
            ("Guerrilla Games", 20024),
            ("Naughty Dog", 20025), 
            ("Electronic Arts", 20026),
            ("Insomniac Games", 20027),
            ("Sledgehammer Games", 20028),
            ("DICE Los Angeles", 20029),
            ("Ubisoft Milan", 20030),
            ("Ubisoft Romania", 20031),
            ("Gameloft", 20032),
            ("Ubisoft Reflections", 20033),
            ("Ubisoft Shanghai", 20034),
            ("Ubisoft Montpellier", 20035),
            ("Ubisoft Annecy", 20036),
            ("Grin", 20037),
            ("Ubisoft Singapore", 20038),
            ("Ubisoft Ukraine", 20039),
            ("Virtuos", 20040),
            ("Next Level Games", 20041),
            ("High Voltage Software", 20042),
            ("Ubisoft Sofia", 20043),
            ("Loot Drop", 20044),
            ("Darkworks", 20045),
            ("Ubisoft Belgrade", 20046),
            ("Ubisoft Barcelona", 20047),
            ("i5works", 20048),
            ("EA Gothenburg", 20049)
        ]
        sql = "INSERT INTO Developer Values(?, ?)"
        _conn.executemany(sql, dev)

        _conn.commit()
        print("success")

    except Error as e:
        _conn.rollback()
        print(e)
    
    print("++++++++++++++++++++++++++++++++++")

def populate_Platforms(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate Platforms")

    try: 
        exclusive = [ #platform(system, exkey, exclusive)
            ("Playstation", 1, 1),
            ("Xbox", 2, 1),
            ("PC", 3, 1),
            ("Nintendo Switch", 4, 1),

            ("PC\nPlaystation", 5, 0),
            ("PC\nXbox", 6, 0),
            ("PC\nNintendo Switch", 7, 0),
            ("Playstation\nXbox", 8, 0),
            ("Playstation\nNintendo Switch", 9, 0),
            ("Xbox\nNintendo Switch", 10, 0),

            ("PC\nPlaystation\nXbox", 11, 0),
            ("Playstation\nXbox\nNintendo Switch", 12, 0),
            ("PC\nPlaystation\nXbox\nNintendo Switch", 13, 0),
            ("PC\nPlaystation\nNintendo Switch", 14, 0),
            ("PC\nXbox\nNintendo Switch", 15, 0)
            
        ]
        sql = "INSERT INTO Platform VALUES(?, ?, ?)"
        _conn.executemany(sql, exclusive)

        _conn.commit()
        print("success")

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def populate_Reviews(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate Platforms")

    try: 
        review = [ #Revews(gameID, rating, resource, comment)
                        # (varchar(30), decimal, varchar, varchar)
            (12, 10, "IGN", "With The Last of Us: Remastered, PlayStation 3's best game just became PlayStation 4's, too."),
            (12, 9, "Metro GameCentral", "Still a stunning achievement in both storytelling and third person adventure, and although this is the definitive version the differences are still minor."),
            (12, 10, "Game Informer", "The punishing world dares you to press on, and the story is an emotional punch to the gut. In short, this is one of the best video games ever made"),
            (18, 8, "IGN", "Call of Duty: Modern Warfare's varied gameplay modes and excellent gunplay suggest the series is headed in a promising direction."),
            (18, 8, "GamesRadar+", "Modern Warfare is fast and frenetic, setting a new benchmark for fidelity and high-pressure FPS action."),
            (17, 8.7, "IGN", "I wanted Marvel's Spider-Man on PS4 to make me feel like Spider-Man: To sail between the highrises of New York City, to nimbly web up hordes of enemies, and tussle with familiar, animal-themed villains. Insomniac Games' first foray into the world of Marvel handily delivers on all of that. But what I didn't expect from Spider-Man was to come away feeling just as fulfilled to have inhabited the life of Peter Parker. Aside from a few odd pacing issues, which momentarily took me out of the experience of being a superhero, and a world of optional missions that don't always quite live up to the heft of the main story, Insomniac has delivered a Spider-Man story that both surprised and delighted me, coupled with gameplay that made me feel like Spider-Man nearly every step of the way. The Wall Crawler's open world doesn't consistently deliver the thrilling moments of its main campaign, but the foundation laid here is undoubtedly a spectacular one."),
            (4, 8.5, "PC Gamer", "Slow, weird, and indulgent, but a true original, and a journey that will linger in your mind long after it's over."),
            (4, 7, "GamesRadar+", "Kojima's mysterious would be epic has its moments but can't carry the weight of expectation."),
            (5, 8.8, "PC Gamer", "It's not flawless, but Overwatch is still one of the best new multiplayer shooters to arrive in years."),
            (5, 10, "IGN", "Overwatch is a masterpiece. A dizzying amalgam of unique characters, stunning style, and compellingly dynamic action."),
            (6, 8, "Game Revolution", "If you are a PS4 or Xbox One owner, Bioshock: The Collection should be in your, um, collection, whether in the 2-disc physical format or digital download. Unfortunately, I’ve read reports that the PC version has issues. (Like bad ones.) As such PC players should wait for the (fingers crossed) eventual patches."),
            (6, 9, "Hobby Consolas", "Three great adventures masterfully ported to Nintendo Switch. They only missing feature is they're not running at 60 fps, but the rest is on spot, showing an adaptation on par with the PS4 and Xbox One remasters. Also, keep in mind that if you buy it, physical or digital, you will need a big microSD, because the download is quite big..."),
            (6, 8, "Metro GameCentral", "Time has worn some holes in each games’ reputation, but these are still three of the most ambitious and daring action games of modern times."),
            (8, 8.4, "PC Gamer", "Although familiar to BF3, but BF4 remains a visually and sonically satisfying, reliably intense FPS. Improved by Commander Mode and a terrific and diverse map set."),
            (8, 9, "GamesRadar+", "Multiplayer shooters don't get better than Battlefield 4. Incredible destruction, smart map design, and solid tech combine to produce a true showcase for PS4 and PC. While solo play still lags behind, it's a big step up from BF3."),
            (2, 9, "Easy Allies", '\0'),
            (2, 9, "IGN", "Star Wars Jedi: Fallen Order makes up for a lot of lost time with a fantastic single-player action-adventure that marks the return of the playable Jedi."),
            (2, 7.3, "PC Gamer", "Technical issues marr an otherwise slick adventure. A must for Star Wars fans."),
            (14, 9, "GamesRadar+", "An open-world that tailors to each and every interest, Horizon: Zero Dawn keeps combat fresh, with an intriguing protagonist to match."),
            (14, 8.6, "PC Gamer", "A classy sandbox that stands out from the pack thanks to its brilliant battles against an array of fantastic beasts."),
            (14, 9.3, "IGN", "Horizon Zero Dawn presents us with a beautiful world full of unforgettable challenges.")
        ]
        sql = "INSERT INTO Reviews VALUES(?, ?, ?, ?)"
        _conn.executemany(sql, review)

        _conn.commit()
        print("success")

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def populate_gamePlay(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate GamePlay")

    try: # GamePlay(gameTitle,      (gameID, website, platform)
        gamePlay = [
            (18, "https://www.twitch.tv/directory/game/Call%20Of%20Duty%3A%20Modern%20Warfare", "Twitch"),
            (18, "https://www.youtube.com/results?search_query=call+of+duty+modern+warfare", "Youtube"),
            (5, "https://www.twitch.tv/directory/game/Overwatch", "Twitch"),
            (5, "https://www.youtube.com/results?search_query=overwatch", "Youtube"),
            (12, "https://www.twitch.tv/directory/game/The%20Last%20of%20Us", "Twitch"),
            (12, "https://www.youtube.com/results?search_query=the+last+of+us+remastered", "Youtube"),
            (6, "https://www.twitch.tv/directory/game/BioShock%3A%20The%20Collection", "Twitch"),
            (6, "https://www.youtube.com/results?search_query=bioshock+the+collection", "Youtube"),
            (2, "https://www.youtube.com/results?search_query=star+wars+jedi+fallen+order", "Youtube"),
            (2, "https://www.twitch.tv/directory/game/Horizon%20Zero%20Dawn", "Twitch"),
            (8, "https://www.youtube.com/results?search_query=battlefield+4", "Youtube")
        ]
        sql = "INSERT INTO GamePlay Values(?, ?, ?)"
        _conn.executemany(sql, gamePlay)

        _conn.commit()
        print("success")

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    
def main():
    database = r"data.sqlite"
    conn = openConnection(database)
    with conn:
        dropTables(conn)
        createTables(conn)
        populateTable_Games(conn)
        populate_Contracts(conn)
        populateTable_DevPub(conn)
        populate_Platforms(conn)
        populate_Reviews(conn)
        populate_gamePlay(conn)
        

    closeConnection(conn, database)


if __name__ == '__main__':
    main()