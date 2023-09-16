var mysql = require('mysql2');
const tls = require('node:tls');
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
        console.log(result);
    });
});

var port = process.env.PORT || 3000

app.get("/imprimir", (req, res) => {
    con.connect(function(err) {
        if (err) throw err;
        con.query("SELECT * FROM persona", function(err,result, fields){
            if(err) throw err;
            console.log(result);
            res.send(result);
        });
    });
})

app.listen(port)
