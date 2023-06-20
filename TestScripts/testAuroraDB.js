import { createConnection } from "mysql2";

const connection = createConnection({
    host: "auroradb-instance-1.cw8yaucd5ypn.us-east-1.rds.amazonaws.com",
    user: "admin",
    password: "Password put while creating AuroraDb Cluster",
    port: 3306,
    database: "Test",
  });


connection.connect((err)=>{
    if(err) throw err
    console.log("Database Connected")
})


const sql =
"CREATE TABLE users (publicAddress VARCHAR(70) PUBLIC KEY, initVector VARCHAR(70), securityKey VARCHAR(70))";
connection.query(sql, function (err, result) {
if (err) throw err;
console.log("Table Created");
});
  
connection.end();    

// var sql = "CREATE TABLE UserKeys (useraddress VARCHAR(255) PRIMARY KEY, initVector VARCHAR(255), securityKey VARCHAR(255))";  
// connection.query(sql, function (err, result) {  
// if (err) throw err;  
// console.log("Table created");  

// });

// var sql = "INSERT INTO UserKeys (useraddress, initVector, securityKey) VALUES ('uhvr78gf8grvbyvbyrbvyr8bvyfub', 'R15M44oRjYaJP+RQmT53E9Nlz9SBQL1HaAKefOt+9Ws', '5evW1aCyDNX6red6Lf0B8KvpnTgdfDZN8pbnQNh1ua8')";  
// connection.query(sql, function (err, result) {  
// if (err) throw err;  
// console.log("1 record inserted");  
// });

// connection.query("SELECT * FROM UserKeys WHERE useraddress = 'uhvr78gf8grvbyvbyrbvyr8bvyfub'", function (err, result) {  
//     if (err) throw err;  
//     console.log(result);
//  })  

// })