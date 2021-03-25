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

    





    
}

//this exports the database connection object 'db', so other scripts can use it
module.exports = db

