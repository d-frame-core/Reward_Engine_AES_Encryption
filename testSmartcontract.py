from web3 import Web3
from dotenv import load_dotenv
from Cryptodome.Hash import SHA512
import os
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime
from datetime import date

load_dotenv()

connectionString=os.getenv("ConnectionString")
contractAddress=os.getenv("Address")
ABI=os.getenv("ABI")
alchemyURL=os.getenv("AlchemyURL")
privateKey=os.getenv("PrivateKey")


def TransferToken():
        if date.today().day !=16:
                return
        
        web3=Web3(Web3.HTTPProvider(alchemyURL))
        contract=web3.eth.contract(address=contractAddress,abi=ABI)

        PublicAddress='0xD8D3f92f44959e91a0001354979e9cb465F1a579'
        SendingAddress='0xD23C7A72CF13ff91e8C53Bc2A217b5Ff82aa9CF3'

        Wallet_from=Web3.to_checksum_address(PublicAddress)
        Wallet_to=Web3.to_checksum_address(SendingAddress)

        token_balance = contract.functions.balanceOf(Wallet_to).call()
        totalTokenSupply=contract.functions.totalSupply().call()
        totakTokens=web3.from_wei(token_balance,'ether')
        # print(totalTokenSupply)
        # print(token_balance)
        # print(totakTokens)
        print(totakTokens)


        # nonce=web3.eth.get_transaction_count(Wallet_from)


        # contract_txn=contract.functions.transfer(
        #        Wallet_to,
        #        10*10**18,
        # ).build_transaction(
        #     {
        #         'chainId': 80001,
        #         'nonce': nonce,
        #         'gas': 100000,
        #         'gasPrice': web3.to_wei("10", "gwei")
        #     }
        # )

        # signed_tx=web3.eth.account.sign_transaction(contract_txn,privateKey)

        # tx_hash=web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # print(web3.to_hex(tx_hash))


if __name__ == "__main__":
    TransferToken()
 