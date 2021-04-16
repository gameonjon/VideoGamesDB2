// load the sqlite3. .verbose() gets extra info for debugging
var sqlite3 = require('sqlite3').verbose()
const Promise = require('bluebird')
const { text } = require('express')


//DBSOURCE is def. of SQLite database file
const DBSOURCE = "./data.sqlite"

//let keyword delcares a variable
//db is Initialization of the SQLite database
    //sqlite3.Database(filename, [model], [callback]). we have (dbsource, ,err).
        //this returns a new DB object and opens it

class db{
    constructor(){
        this.db = new sqlite3.Database(DBSOURCE, (err) => {  //here '(err)' is the function that follows '=>'
            if(err){    //callback 
                // Cannot open Database
                console.error(err.message)
                throw err
            }else{
                console.log('Connnected to the SQLite database.')
            }
        })
    }


    //========= for drop down menu
    all(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, rows) => {
                if(err){
                    console.log('Error running sql: ' + sql)
                    console.log(err)
                    reject(err)
                }   else{
                    resolve(rows)
                }
            })
        })
    }

    allGames() {    //SQL  for query. call to all() 
        return this.all(
            "SELECT DISTINCT g_title as Title, g_year as Year, g_genre as Genre " +
                "FROM Games", [])
    }

    allReviews() {
        return this.all(
            "SELECT g_title AS Game_Title, r_rating AS Rating, r_comment AS Review, r_resource AS Resource" +
            " FROM Reviews, Games" +
            " WHERE r_gameID = g_gameID", [])
            //"GROUP BY r_gameID" +
    }

    allCreators() {
        return this.all(
            "SELECT DISTINCT g_title AS GameTitle, p_name AS Publisher, d_name AS Developer" +
                " FROM Games, Developer, Publisher, Contracts" +
                " WHERE g_gameID = c_gameID AND" +
                    " c_devkey = d_devkey AND" +
                    " c_pubkey = p_pubkey" +
            " UNION" +
            " SELECT DISTINCT g_title AS GameTitle, p_name AS Publisher, c_devkey AS Developer" +
                " FROM Games, Developer, Publisher, Contracts" +
                " WHERE g_gameID = c_gameID AND" +
                    " p_pubkey = c_pubkey AND" +
                    " c_devkey NOT IN (SELECT c_devkey" +
                    " FROM Contracts, Publisher, Developer, Games" +
                    "  WHERE p_pubkey = c_pubkey AND" +
                    " c_devkey = d_devkey AND" +
                    " g_gameID = c_gameID)" +
            " UNION" +
            " SELECT DISTINCT g_title AS GameTitle, c_pubkey AS Publisher, d_name AS Developer" +
                " FROM Games, Developer, Publisher, Contracts" +
                " WHERE g_gameID = c_gameID AND" +
                    " d_devkey = c_devkey AND" +
                    " c_pubkey NOT IN (SELECT c_pubkey" +
                    "  FROM Contracts, Publisher, Developer, Games" +
                    " WHERE p_pubkey = c_pubkey AND" +
                    " c_devkey = d_devkey AND" +
                    " g_gameID = c_gameID)", [])
    }
    
    allGamePlatforms(){
        return this.all(
            "SELECT DISTINCT g_title AS GameTitle, pf_system AS Platform" +
            " FROM Games, Platform" +
            " WHERE g_exkey = pf_exkey", [])
    }

    allPlatforms(){
        return this.all(
            
        )
    }

    // insertNewGame(gTitle, gYear, gGenre, pPub, dDev, pfCB){
    //     return this.all(
    //         "INSERT INTO Games (g_title, g_year, g_genre) VALUES(?, ?, ?); " + 
    //         "UPDATE Games SET g_exkey = (SELECT pf_exkey FROM Platform WHERE pf_system = ?) WHERE g_title = ?; " +
    //         "INSERT INTO Publisher (p_name) VALUES(?); " +
    //         "INSERT INTO Developer (d_name) VALUES(?); " +
    //         "INSERT INTO Contracts (c_gameID, c_pubkey, c_devkey) " + 
    //             "SELECT g_gameID, p_pubkey, d_devkey " +
    //                     "FROM Games, Publisher, Developer " +
    //                     "WHERE g_title = ? AND " +
    //                         "p_name = ? AND " +
    //                         "d_name = ?", [gTitle, gYear, gGenre, pfCB, gTitle, pPub, dDev, gTitle, pPub, dDev])
    // }

    insertNewGame(gTitle, gYear, gGenre){
        return this.all(
            "INSERT INTO Games (g_title, g_year, g_genre) VALUES(?, ?, ?)", [gTitle, gYear, gGenre]
        )
    }
    updateNewGame(gTitle, pCB){
        return this.all(
            "UPDATE Games SET g_exkey = (SELECT pf_exkey FROM Platform WHERE pf_system = ?) WHERE g_title = ?", [gTitle, pCB]
        )
    }
    insertPublisher(pPub){
        return this.all(
            "INSERT INTO Publisher (p_name) VALUES(?)", [pPub]
        )
    }
    insertDeveloper(dDev){
        return this.all(
            "INSERT INTO Developer (d_name) VALUES(?)", [dDev]
        )
    }
    insertContract(gTitle, pPub, dDev){
        return this.all(
            "INSERT INTO Contracts (c_gameID, c_pubkey, c_devkey) " + 
                "SELECT g_gameID, p_pubkey, d_devkey " +
                        "FROM Games, Publisher, Developer " +
                        "WHERE g_title = ? AND " +
                            "p_name = ? AND " +
                            "d_name = ?", [gTitle, pPub, dDev]
        )

    }


    //================ GET CHECKBOX VALUE
    getCheckboxValues(checkboxArr){
        //.join has a defualt to place "," between values;
            //for different option change .join("")
        var vals = checkboxArr.join();
        return vals;
    }





    
}

//this exports the database connection object 'db', so other scripts can use it
module.exports = db

