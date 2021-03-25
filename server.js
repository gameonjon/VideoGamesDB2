// Create express app
var express = require("express")
var app = express()
var md5 = require("md5")    //for new user... md5 hashes the password created

const db = require("./database.js")   //we can probably change this with the VideoGame DB
var videogames = new db()

//'body-parser' middleware module tries to parse the body content (URL en. or json) of post request
    // and store in 'req.body' object
var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Server port
var HTTP_PORT = 8000

app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);

    next();
});

// Start server
app.listen(HTTP_PORT, () => {
    console.log("Server running on port %PORT%".replace("%PORT%", HTTP_PORT))
});
// Root endpoint
app.get("/", (req, res, next) => {
    res.json({"message":"Ok"})
});





/*Middleware functions are functions that have access to the request object 0
    (req), the response object (res), and the next middleware function in 
    the application’s request-response cycle. The next middleware function 
    is commonly denoted by a variable named next.
Middleware functions can perform the following tasks:
    Execute any code.
    Make changes to the request and the response objects.
    End the request-response cycle.
    Call the next middleware function in the stack.*/

//======================================
// Insert here other API endpoints
//======================================

app.get("/api/games", (req, res, next) => {
    videogames.allGames()
        .then((games) => {
            res.json({  //json payload contains the data pack. denoted with {} in query string
                "message": "success",
                "data": games
            })
        })
        .catch((err) => {
            res.status(400).json({ "error":err.message });
            return;
        })        
});

app.get("/api/menu/:opt", (req, res, next) => {
    if(req.params.opt == "Games"){  //if the menu option =="games"
        videogames.allGames()
        .then((gtable) => {
            res.json({
                "message": `success`,
                "data": gtable
            })
        })
        .catch((err) => {
            res.status(400).json({ "error": err.message });
            return;
        })  
    }
    else if(req.params.opt =="Reviews"){
        videogames.allReviews()
        .then(rtable => {
            res.json({
                "message": `success`,
                "data":rtable
            })
        })
        .catch(err => {
            res.status(400).json({"error": err.message})
        })
    }
});







// Default response for any other request
app.use(function(req, res){
    res.status(404);
});