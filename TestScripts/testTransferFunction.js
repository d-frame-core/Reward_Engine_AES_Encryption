import * as dotenv from "dotenv";
import { ethers } from "ethers";
dotenv.config();

const contractAddress = process.env.Address;
const ABI = process.env.ABI;
const alchemyURL = process.env.AlchemyURL;
const privateKey = process.env.PrivateKey;

const tokenTransfer = async () => {
  const provider = new ethers.JsonRpcProvider(alchemyURL);
  const signer = new ethers.Wallet(privateKey, provider);
  const contract = new ethers.Contract(contractAddress, ABI, signer);

  //Wallet address of the user
  const Wallet_to = "0xD23C7A72CF13ff91e8C53Bc2A217b5Ff82aa9CF3";

  const amount = ethers.parseUnits("0.5", 18);

  contract.transfer(Wallet_to, amount).then((tx) => {
    console.log(tx);
  });
};

tokenTransfer();
