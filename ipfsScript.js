import { create } from "ipfs-http-client";
import { readFile } from "fs";

const ipfs1 = create(new URL("http://127.0.0.1:5001"));

const addingIPFS = async () => {
  readFile("./encrypted.bin", async (err, dataFile) => {
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
