// Create express app
var express = require("express")
var app = express()
var db = require("./database.js")   //we can probably change this with the VideoGame DB
var videogames = new db()

//'body-parser' middleware module tries to parse the body content (URL en. or json) of post request
    // and store in 'req.body' object
    //Notice how app.use(function below only focuses on passing to 'res')
var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());   //might have to put this back in


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
    // console.dir(res.headersSent)    //false 
    res.json({"message":"Ok"})
    // console.dir(res.headersSent)    //true
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

app.get("/api/game/:id", (req, res, next) =>{
    var params = [req.params.id]
    // videogames.db.get()
    videogames.getGame(params)
        .then((game) =>{
            res.json({
                "message":"success",
                "data":game
            })
        })
        .catch((err) =>{
            res.status(400).json({ "error":err.message })
            return;
        })
});

// app.get("api/Platforms", (req, res, next) => {
//     videogames.allPlatforms()
//         .then((platforms) => {
//             res.json({
//                 "message": "success", 
//                 "data": platforms
//             })
//         })
//         .catch((err) => {
//             res.status(400).json({ "error":err.message });
//             return;
//         })
// });

app.get("/api/menu/:opt", (req, res, next) => {
    if(req.params.opt == "Games"){  //if the menu option =="games"
        videogames.allGames()
        .then((gtable) => {
            res.json({ //json payload contains the data pack. denoted with {} in query string
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
    else if(req.params.opt == "PubDev"){
        videogames.allCreators()
        .then(pdTable => {
            res.json({
                "message": `success`,
                "data":pdTable
            })
        })
        .catch(err => {
            res.status(400).json({"error":err.message})
        })
    }
    else if(req.params.opt == "Platform"){
        videogames.allGamePlatforms()
        .then(pTable => {
            res.json({
                "message": `success`,
                "data":pTable
            })
        })
        .catch(err => {
            res.status(400).json({"error":err.message})
        })
    }
});

//======================= Create new Game entry
app.post("/api/newGames/", (req, res, next) => {
    var errors=[]

    //NOTE: the check mandatory fields were not looked into on POSTMAN when using a
        //body x-www-url.... input. look into what these fields are actually for
    if(!req.body.GameTitle){
        errors.push("No Title entry");
    }
    if(!req.body.ReleaseYear){
        errors.push("No Year specified");
    }
    if(!req.body.Genre){
        errors.push("No genre specified");
    }
    if(!req.body.Publisher){
        errors.push("No Publisher specified");
    }
    if(!req.body.Developer){
        errors.push("No Developer specified")
    }
    //also need to check for platform entry!!!!!!!!!!!!!!!!!!!
    if(errors.length){//Send list of errors
        res.status(400).json({ "error":errors.join(",") });
        return;
    }

    var data = {
        gameTitle: req.body.GameTitle,
        year: req.body.ReleaseYear,
        genre: req.body.Genre,
        publisher: req.body.Publisher,
        developer: req.body.Developer,
       // platformCB: req.body.platOpt   //this should get array for checkboxes

        //this should replace the array of req.body.platOpt and place it in a single
            //string for data.platformCB to use for the SQL query
        //data.platformCB = videogames.getCheckboxValues(req.body.platOpt)
        platformCB: videogames.getCheckboxValues(req.body.platOpt)
    }    

    // var sql = "INSERT INTO Games (g_title, g_year, g_genre) VALUES(?, ?, ?)"
    // console.log(sql)
    // var params = [data.gameTitle, data.year, data.genre]
    // videogames.db.run(sql, params, function (err, result){
    //     if (err){
    //         res.status(400).json({"error": err.message})
    //         return;
    //     }
    //     res.json({  // everything worked
    //         "message": "success: new gametitle\n",
    //         "\ndata": data.gameTitle
    //     })
    // });

    // videogames.insertNewGame(data.gameTitle, data.year, data.genre, data.publisher, data.developer, data.platformCB)
    //     .then(insertNew => {
    //         res.json({
    //             "message":`Success! New Game Added`,
    //             "data":insertNew
    //         })
    //     })
    //     .catch(err => {
    //         res.status(400).json({"error":err.message})
    //     })

    

    videogames.insertNewGame(data.gameTitle, data.year, data.genre)
        .catch(err => {
            res.status(400).json({"error":err.message})
        })
    videogames.updateNewGame(data.gameTitle, data.platformCB)
        .catch(err => {
            res.status(400).json({"error":err.message})
        })
    videogames.insertPublisher(data.publisher)
        .catch(err => {
            res.status(400).json({"error":err.message})
        })
    videogames.insertDeveloper(data.developer)
        .catch(err => {
            res.status(400).json({"error":err.message})
        })
    videogames.insertContract(data.gameTitle, data.publisher, data.developer)
        .then(() => {
            res.json({
                "message":`Success! inserted new game`,
                "data":data.gameTitle
            })            
        })
        .catch(err => {
            res.status(400).json({"error":err.message})
        })
});

//===========================UPDATE GAME
app.patch("/api/game/:id", (req, res, next) => {
    //whatever the req.body. values are named are what they should be 
        //exactly when using POSTMAN.com for PATCH request testing
    var data = {
        game: req.body.gameTitle,
        year: req.body.releaseYear,
        genre: req.body.genre,
        gameID: req.params.id,
        platform: req.body.platformCB   //POSTman still requires it to be "platformCB" when called to change
    }
        // console.log(req.body.platformCB)    //not sure why already works
    // console.log(req.body.GameTitle)

    videogames.updateGame(data.game, data.year, data.genre, data.gameID)
    videogames.updateGamePf(data.platform, data.gameID)
        .then(() => {
            res.json({
                message:`Success! Updated current game in Database`,
                data: data,
                changes: this.changes
            })            
        })
        .catch(err => {
            res.status(400).json({"error":err.message})
            return;
        })
});

//=================DELETE GAME
app.delete("/api/game/:id", (req, res, next) =>{
    videogames.deleteGame(req.params.id)
        .then(() =>{
            res.json({
                message: `Success in deleting game`,
                changes: this.changes   //return number of rows affected
            })
            //if user not found/deleted, value = 0
        })
        .catch(err =>{
            res.status(400).json({"error":res.message})
            return;
        })
})



// Default response for any other request
app.use(function(req, res){
    res.status(404);
});