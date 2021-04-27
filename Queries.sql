--SQLITE SCRATCH SHEET

-- games table(not used)
SELECT DISTINCT g_title
    FROM Games

SELECT * FROM Games
    WHERE g_gameID = 7

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
        


--======================================
-- for app.post in server.js
--======================================

--example of inserts below
INSERT INTO Games (g_title, g_year, g_genre) VALUES("Resident Evil 5", '2009-05-03', "Survival horror");
UPDATE Games
    SET g_exkey = (SELECT pf_exkey FROM Platform WHERE pf_system = 'PC,Xbox,Nintendo')
    WHERE g_title = 'Resident Evil 5';
INSERT INTO Publisher (p_name) VALUES("Capcom");
INSERT INTO Developer (d_name) VALUES("Capcom");
INSERT INTO Contracts (c_gameID, c_pubkey, c_devkey)
    SELECT g_gameID, p_pubkey, d_devkey
            FROM Games, Publisher, Developer
            WHERE g_title = 'Resident Evil 5' AND
                p_name = 'Capcom' AND
                d_name = 'Capcom';


INSERT INTO Games (g_title, g_year, g_exkey, g_genre) VALUES(?, ?, ?, ?)
UPDATE Games SET g_exkey = (SELECT pf_exkey FROM Platform WHERE pf_system = ?)
    WHERE g_title = ?
INSERT INTO Publisher (p_name) VALUES(?)
INSERT INTO Developer (d_name) VALUES(?)
INSERT INTO Contracts (c_gameID, c_pubkey, c_devkey)
    SELECT g_gameID, p_pubkey, d_devkey
            FROM Games, Publisher, Developer
            WHERE g_title = ? AND
                p_name = ? AND
                d_name = ?




-- Triggers part 2
CREATE TRIGGER insert_GCPD INSTEAD OF INSERT ON Games
FOR EACH ROW
BEGIN
    INSERT INTO Contracts (c_gameID, c_pubkey, c_devkey) 
        SELECT NEW.g_gameID, NEW.p_pubkey, NEW.d_devkey
            FROM Games, Publisher, Developer
            WHERE g_title = NEW.g_title AND
                p_name = NEW.p_name AND
                d_name = NEW.d_name
END

CREATE TRIGGER insertGCPD AFTER INSERT ON Games
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT * FROM Publisher
                    WHERE p_name = 'Capcom')
    BEGIN
        INSERT INTO Publisher (p_name) VALUES('Capcom')
    END
    IF NOT EXISTS (SELECT * FROM Developer
                    WHERE d_name = 'Capcom')
    BEGIN
        INSERT INTO Developer (d_name) VALUES('Capcom')
    END

    INSERT INTO Contracts (c_gameID, c_pubkey, c_devkey) 
        SELECT NEW.g_gameID, p_pubkey, d_devkey
            FROM Games, Publisher, Developer
            WHERE g_title = NEW.g_title AND
                p_name = 'Capcom' AND
                d_name = 'Capcom'
END

DROP TRIGGER insertGCPD

SELECT insert_GCPD, is_disabled FROM sys.triggers

--we also need a trigger to control the contracts update
--this will go in VideoGame.py for DB setup



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

DROP VIEW GCPD

INSERT INTO GCPD




-- PATCH request for direct game values (and Platform) only        
UPDATE Games SET
    g_title = COALESCE(?, g_title),
    g_year = COALESCE(?, g_year),
    g_genre = COALESCE(?, g_genre)
    WHERE g_gameID = ?
    --Pretty sure that COALESCE is an SQL Server Function Only, wont work if you run it here
UPDATE Games
    SET g_exkey = COALESCE(SELECT pf_exkey FROM Platform WHERE pf_system = ?, g_exkey)
    WHERE g_gameID = ?;

            --for testing:
UPDATE Games SET
    g_title = "Dying Retribution",
    g_genre = "Action-Horror"
    WHERE g_gameID = 7
UPDATE Games
    SET g_exkey = (SELECT pf_exkey FROM Platform WHERE pf_system = 'PC,Xbox,Nintendo')
    WHERE g_gameID = 7;


-- DELETE request for Games
DELETE FROM Games WHERE g_gameID = 7;

DELETE FROM Games WHERE g_gameID = ?
        






