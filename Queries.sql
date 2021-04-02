--SQLITE SCRATCH SHEET

-- games table(not used)
SELECT DISTINCT g_title
    FROM Games

-- for Reviews table
SELECT g_title AS Game_Title, r_rating AS Rating, r_comment AS Review, r_resource AS Resource
    FROM Reviews, Games
    WHERE r_gameID = g_gameID
    GROUP BY r_gameID

--Publisher and Dev
SELECT DISTINCT g_title AS GameTitle, p_name AS Publisher, d_name AS Developer
    FROM Games, Developer, Publisher, Contracts
    WHERE g_gameID = c_gameID AND
        c_devkey = d_devkey AND
        c_pubkey = p_pubkey
UNION
SELECT DISTINCT g_title AS GameTitle, p_name AS Publisher, c_devkey AS Developer
    FROM Games, Developer, Publisher, Contracts
    WHERE g_gameID = c_gameID AND
        p_pubkey = c_pubkey AND
        -- c_devkey = NULL
        c_devkey NOT IN (SELECT c_devkey
                            FROM Contracts, Publisher, Developer, Games
                            WHERE p_pubkey = c_pubkey AND
                                c_devkey = d_devkey AND
                                g_gameID = c_gameID)
UNION
SELECT DISTINCT g_title AS GameTitle, c_pubkey AS Publisher, d_name AS Developer
    FROM Games, Developer, Publisher, Contracts
    WHERE g_gameID = c_gameID AND
        d_devkey = c_devkey AND
        c_pubkey NOT IN (SELECT c_pubkey
                            FROM Contracts, Publisher, Developer, Games
                            WHERE p_pubkey = c_pubkey AND
                                c_devkey = d_devkey AND
                                g_gameID = c_gameID)
    ORDER BY g_title



-- Platform table
SELECT DISTINCT g_title AS GameTitle, pf_system AS Platform
    FROM Games, Platform
    WHERE g_exkey = pf_exkey

-- Platform table w/o games
SELECT DISTINCT pf_system
    FROM Platform
        


-- for app.post in server.js
--======================================

--first games table
INSERT INTO Games (g_title, g_year, g_genre) VALUES(?, ?, ?)
--Publishers table
INSERT INTO Publisher (p_name) VALUES(?)
--Dev table
INSERT INTO Developer (d_name) VALUES(?)
--next contracts table (wont show to client but need this for future references
-- of many to many relationships
INSERT INTO Contracts(c_gameID, c_pubkey, 



--example of inserts above
INSERT INTO Games (g_title, g_year, g_genre) VALUES("Resident Evil 5", '2009-05-03', "Survival horror")

INSERT INTO Publisher (p_name) VALUES("Capcom")

INSERT INTO Developer (d_name) VALUES("Capcom")

INSERT INTO Contracts (c_gameID, c_pubkey, c_devkey) 

DELETE FROM Games
    WHERE g_title = "Resident Evil 5"

--we also need a trigger to control the contracts update
--this will go in VideoGame.py for DB setup
CREATE TRIGGER insert_GCPD AFTER INSERT ON Games

CREATE TRIGGER insert_GCPD INSTEAD OF INSERT ON Games
FOR EACH ROW
BEGIN
    INSERT INTO Games(




CREATE VIEW GCPD(gameTitle, gameYear, genre, exKey, pubName, devName) AS
    SELECT g.g_title, g.g_year, g.g_genre, g.g_exkey, p.p_name, d.d_name
        FROM Games g, Publisher p, Developer d, Contracts c
        WHERE g.g_gameID = c.c_gameID AND
        c.c_devkey = d.d_devkey AND
        c.c_pubkey = p.p_pubkey
    UNION
    SELECT g.g_title, g.g_year, g.g_genre, g.g_exkey, p.p_name, d.d_name
        FROM Games g, Publisher p, Developer d, Contracts c
        WHERE g.g_gameID = c.c_gameID AND
        c.c_pubkey = p.p_pubkey AND
        c.c_devkey NOT IN (SELECT c_devkey
                            FROM Contracts, Publisher, Developer, Games
                            WHERE p_pubkey = c_pubkey AND
                                c_devkey = d_devkey AND
                                g_gameID = c_gameID)
    UNION
    SELECT g.g_title, g.g_year, g.g_genre, g.g_exkey, p.p_name, d.d_name
        FROM Games g, Publisher p, Developer d, Contracts c
        WHERE g.g_gameID = c.c_gameID AND
        c.c_devkey = d.d_devkey AND
        c.c_pubkey NOT IN (SELECT c_pubkey
                            FROM Contracts, Publisher, Developer, Games
                            WHERE p_pubkey = c_pubkey AND
                                c_devkey = d_devkey AND
                                g_gameID = c_gameID)






