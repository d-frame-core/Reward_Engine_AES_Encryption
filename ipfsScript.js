import { create } from "ipfs-http-client";
import { readFile, writeFile } from "fs";
// import { TextDecoder } from "textEncoding";

const ipfs1 = create(new URL("http://127.0.0.1:5001"));

const addingIPFS = async () => {
  readFile("./userdata.bin", async (err, dataFile) => {
    if (err) throw err;
    let result1 = await ipfs1.add(
      {
        content: dataFile,
      },
      { pin: true }
    );
    console.log(result1.path);
  });
};

addingIPFS();

// for await (const { cid, type } of ipfs1.pin.ls()) {
//   console.log({ cid, type });
// }

// for await (const chunk of ipfs1.cat("QmcyMBesUCACgLrbYDD8kGq3nwT2eBUy326JEXs67jUUrg")) {
//     let dataFile=chunk
//     writeFile("./userdata.bin", dataFile, (err) =>{
//       if(err) throw err;
//       else{
//         console.log("File written successfully");
//       }
//     })
//   }