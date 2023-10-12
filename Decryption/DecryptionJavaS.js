import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { QueryCommand } from "@aws-sdk/lib-dynamodb";
import { writeFile } from "fs";
import { create } from "ipfs-http-client";
import { spawn } from "child_process";
const Redis = require("ioredis");

//Connecting local DyanmoDB
// const dbclient = new DynamoDBClient({ region: "local", endpoint: 'http://localhost:8000' });

const ipfs = create(new URL("http://127.0.0.1:5001"));

const redisPassword = "thisismynewpassword";

const redisClient = new Redis({
  host: "localhost",
  port: 6379,
  password: redisPassword,
  db: 1,
});

//Connecting local Ipfs Node

async function getIPFSCIDs(userAddress) {
  try {
    return await redisClient.zrange(userAddress, 0, -1);
  } catch (error) {
    console.error(`Error retrieving IPFS CIDs for ${userAddress}: ${error}`);
    return [];
  }
}

//delay for waiting for results to come from python to node js
const delay = async (ms = 1000) =>
  new Promise((resolve) => setTimeout(resolve, ms));

//Pushing Ipfs cid in this array
// const userCid = [];

// //Pushing Ipfs Cid in the array userCid
// const pushCid = async () => {
//   const data = await dbclient.send(new QueryCommand(params));
//   data.Items.forEach(async (item, index) => {
//     const Cid = await item.IpfsCid;
//     const finalCid = await Cid.replace(/(\n)/gm, "");
//     userCid.push(finalCid);
//   });
// };

//Loop through the array(userCid) and fetching the data from ipfs Node to write in userdata.bin then calling
//"DecryptionPython.py" through child process to result the decrypted orignal data
const fetchFromIpfs = async (userAddress) => {
  const userCid = await getIPFSCIDs(userAddress);
  for (var i = 0; i < userCid.length; i++) {
    const cid = await userCid[i].decode();
    for await (const chunk of ipfs.cat(cid)) {
      console.log("i am here.");
      let dataFile = chunk;
      writeFile("./userdata.bin", dataFile, (err) => {
        if (err) throw err;
        else {
          console.log("File written successfully");
        }
      });
    }
    await delay(2000);
    console.log("Process Started");
    const child = spawn("python", ["./DecryptionPython.py"]);
    child.stdout.on("data", function (data) {
      console.log(data.toString());
    });
    child.on("exit", (code) => {
      console.log(`child process exited with code ${code}`);
    });
    await delay(10000);
  }
};

// pushCid();

// await delay(1000);

fetchFromIpfs(userAddress);
