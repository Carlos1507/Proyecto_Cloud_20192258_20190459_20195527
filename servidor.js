var mysql = require('mysql2');
const tls = require('node:tls');
const bodyParser = require("body-parser");
const express = require('express');
var app = express();

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "root",
    database:"happyhierba"
  });

con.connect(function(err) {
    if (err) throw err;
    con.query("SELECT * FROM persona", function(err,result, fields){
        if(err) throw err;
       // console.log(result);
    });
});

var port = process.env.PORT || 3000

app.get("/imprimir", (req, res) => {
    con.query("SELECT * FROM persona", function(err,result, fields){
        if(err) throw err;
        console.log(result);
        res.send(result);
    });
})

app.get("/validar/:user/:password", (req, res) => {
    let user = req.params.user;
    let password = req.params.password;
    let sql = "SELECT * FROM happyhierba.persona where (correo= ? and contrasenia= ?)"
    let params = [user, password];
    con.query(sql, params, function (err, result) {
        if(err) throw err;
        res.send(result);
    })
});

// usar bodyParser.json() cuando se manda como raw -> json
// usar bodyParser.urlencoded({extended: true}) cuando se manda como x-www-form-unlencoded

app.post("/validarPOST", bodyParser.json(), function (req, res) {
    let user = req.body.user;
  
    let password = req.body.password;
    let sql = "SELECT * FROM happyhierba.persona where (correo= ? and contrasenia= ?)"
    let params = [user, password];
    con.query(sql, params, function (err, result) {
        if(err) throw err;
        res.send(result);
        console.log(result);
    })
});

app.listen(port)