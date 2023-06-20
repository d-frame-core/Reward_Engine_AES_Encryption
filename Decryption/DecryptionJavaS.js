import { DynamoDBClient } from "@aws-sdk/client-dynamodb"; 
import { QueryCommand } from "@aws-sdk/lib-dynamodb";
import {writeFile } from "fs";
import { create } from "ipfs-http-client";
import { spawn } from "child_process"

//Connecting local DyanmoDB
const dbclient = new DynamoDBClient({ region: "local", endpoint: 'http://localhost:8000' });

//Connecting local Ipfs Node
const ipfs = create(new URL("http://127.0.0.1:5001")); 

//Parameters for connecting to DyanmoDB Table
//KeyConditionExpression is the Key("UserPublicAddress") provided to query in the DB
const params = {
    TableName: "IPFS_USER-CID",
    KeyConditionExpression: "UserPublicAddress= :addrs",
    ExpressionAttributeValues: {
        ":addrs": "0xA0D4594DC85b492dfAc756C6D4f6398e3a005767"
    }
}

//delay for waiting for results to come from python to node js
const delay = async (ms = 1000) =>
  new Promise(resolve => setTimeout(resolve, ms))

//Pushing Ipfs cid in this array
const userCid=[];

//Pushing Ipfs Cid in the array userCid
const pushCid = async () =>{
  const data = await dbclient.send(new QueryCommand(params));
  data.Items.forEach(async (item,index)=>{
  const Cid = await item.IpfsCid
  const finalCid = await Cid.replace(/(\n)/gm, "");
  userCid.push(finalCid)
  })
}
 
//Loop through the array(userCid) and fetching the data from ipfs Node to write in userdata.bin then calling
//"DecryptionPython.py" through child process to result the decrypted orignal data
const fetchFromIpfs = async () => {
  for(var i=0;i<userCid.length;i++){
    console.log(userCid[i])
    for await (const chunk of ipfs.cat(userCid[i])){
      console.log("i am here.")
      let dataFile=chunk
      writeFile("./userdata.bin", dataFile, (err) =>{
        if(err) throw err;
        else{
          console.log("File written successfully");
        }
      })
    }
    await delay(2000)
    console.log("Process Started")
    const child = spawn('python', ["./DecryptionPython.py"])
    child.stdout.on('data', function(data) {
        console.log(data.toString())
    })
    child.on('exit',(code)=>{
      console.log(`child process exited with code ${code}`);
    })
    await delay(10000)
  }
};

pushCid();

await delay(1000)

fetchFromIpfs.apply(this,userCid);
